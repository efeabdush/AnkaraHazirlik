from __future__ import annotations

import multiprocessing
import os
import re
import tempfile
import threading
from collections import Counter
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from starlette.concurrency import run_in_threadpool

from ..config import settings
from ..rate_limit import limit_transcribe_concurrency, rate_limit_transcribe
from .security import require_human

router = APIRouter(prefix="/api", tags=["transcription"])

_model = None
_model_lock = threading.Lock()
_allowed_types = {
    "audio/webm": ".webm",
    "video/webm": ".webm",
    "audio/ogg": ".ogg",
    "audio/mp4": ".m4a",
    "audio/mpeg": ".mp3",
    "audio/wav": ".wav",
    "audio/x-wav": ".wav",
}

_filler_pattern = re.compile(r"^(?:u+m+|u+h+|e+r+m+|h+m+|m+|a+h+|e+r+)$", re.IGNORECASE)


def _clean_spoken_word(value: str) -> str:
    return re.sub(r"[^a-z']", "", value.lower())


def _analyze_disfluencies(words: list[dict]) -> dict:
    """Approximate hesitation events from Whisper word timing and confidence."""
    filler_words: Counter[str] = Counter()
    events: list[dict] = []
    word_repetitions = 0
    hesitation_pauses = 0
    elongations = 0
    unclear_words = 0
    previous_token = ""
    previous_raw = ""
    previous_was_filler = False
    previous_end: float | None = None

    for item in words:
        raw = str(item.get("word", "")).strip()
        token = _clean_spoken_word(raw)
        start = float(item.get("start", 0) or 0)
        end = float(item.get("end", start) or start)
        probability = float(item.get("probability", 1) or 0)
        gap = start - previous_end if previous_end is not None else 0

        if 0.45 <= gap < 1.2 and previous_raw and not re.search(r"[.!?]$", previous_raw) and not previous_was_filler:
            hesitation_pauses += 1
            events.append({"type": "hesitation_pause", "time": round(start, 2), "label": f"{gap:.1f} sn duraklama"})

        is_filler = bool(token and _filler_pattern.fullmatch(token))
        if is_filler:
            canonical = "hmm" if token.startswith(("h", "m")) else "erm" if token.startswith("e") else "ah" if token.startswith("a") else "uh" if "h" in token else "um"
            filler_words[canonical] += 1
            events.append({"type": "filler", "time": round(start, 2), "label": raw or canonical})
        elif token and token == previous_token and gap < 0.9:
            word_repetitions += 1
            events.append({"type": "word_repetition", "time": round(start, 2), "label": raw})

        if is_filler and end - start >= 0.75:
            elongations += 1
            events.append({"type": "elongation", "time": round(start, 2), "label": raw or token})
        if token and not is_filler and probability < 0.35:
            unclear_words += 1
            events.append({"type": "unclear", "time": round(start, 2), "label": raw})

        if token and not is_filler:
            previous_token = token
        previous_raw = raw
        previous_was_filler = is_filler
        previous_end = max(end, previous_end or 0)

    return {
        "filler_count": sum(filler_words.values()),
        "filler_words": dict(filler_words),
        "word_repetition_count": word_repetitions,
        "hesitation_pause_count": hesitation_pauses,
        "elongation_count": elongations,
        "unclear_word_count": unclear_words,
        "disfluency_events": events[:40],
    }


def _build_model():
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise RuntimeError("Yerel konuşma modeli kurulu değil. backend bağımlılıklarını yeniden kur.") from exc
    return WhisperModel(
        settings.whisper_model,
        device=settings.whisper_device,
        compute_type=settings.whisper_compute_type,
        download_root=str(settings.storage_dir / "models"),
    )


def _get_model():
    """Keep the model warm locally, but never pin it in Railway's 1 GB RAM."""
    global _model
    if settings.is_production:
        return _build_model()
    if _model is not None:
        return _model
    with _model_lock:
        if _model is None:
            _model = _build_model()
        return _model


def _transcribe_with_model(model, path: Path, topic_hint: str) -> dict:
    prompt = "Transcribe the English speech faithfully. Keep spoken filler words such as um, uh, erm, and hmm when audible."
    if topic_hint.strip():
        prompt += f" The speaking topic is: {topic_hint.strip()[:500]}"
    segments, info = model.transcribe(
        str(path),
        language="en",
        beam_size=max(1, settings.whisper_beam_size),
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 500},
        condition_on_previous_text=True,
        initial_prompt=prompt,
        hotwords="um uh erm hmm mm ah er hesitation",
        word_timestamps=True,
    )
    text_parts: list[str] = []
    segment_data: list[dict] = []
    previous_end = 0.0
    long_pauses = 0
    speech_duration = 0.0
    word_data: list[dict] = []
    for segment in segments:
        clean = segment.text.strip()
        if clean:
            text_parts.append(clean)
        start, end = float(segment.start), float(segment.end)
        if start - previous_end >= 1.2:
            long_pauses += 1
        speech_duration += max(0.0, end - start)
        previous_end = end
        segment_data.append({"start": round(start, 2), "end": round(end, 2), "text": clean})
        for word in segment.words or []:
            word_data.append({
                "word": word.word,
                "start": round(float(word.start), 2),
                "end": round(float(word.end), 2),
                "probability": round(float(word.probability), 3),
            })
    text = " ".join(text_parts).strip()
    duration = float(getattr(info, "duration", 0) or previous_end)
    disfluencies = _analyze_disfluencies(word_data)
    return {
        "text": text,
        "language": str(getattr(info, "language", "en")),
        "language_probability": round(float(getattr(info, "language_probability", 0)), 3),
        "duration_sec": round(duration),
        "speech_duration_sec": round(speech_duration),
        "long_pause_count": long_pauses,
        "segments": segment_data,
        **disfluencies,
    }


def _transcription_worker(path: str, topic_hint: str, connection) -> None:
    """Load Whisper in a disposable process so native RAM is returned to Railway."""
    try:
        result = _transcribe_with_model(_build_model(), Path(path), topic_hint)
        connection.send({"ok": True, "result": result})
    except BaseException as exc:  # noqa: BLE001
        connection.send({"ok": False, "error": f"{type(exc).__name__}: {str(exc)[:500]}"})
    finally:
        connection.close()


def _run_isolated_transcription(path: Path, topic_hint: str) -> dict:
    context = multiprocessing.get_context("spawn")
    parent_connection, child_connection = context.Pipe(duplex=False)
    process = context.Process(
        target=_transcription_worker,
        args=(str(path), topic_hint, child_connection),
        name="whisper-transcription",
    )
    process.start()
    child_connection.close()
    timeout = max(30, settings.whisper_worker_timeout_seconds)
    try:
        if not parent_connection.poll(timeout):
            process.terminate()
            process.join(timeout=5)
            raise RuntimeError(f"Konuşma modeli {timeout} saniye içinde yanıt vermedi.")
        try:
            payload = parent_connection.recv()
        except EOFError as exc:
            process.join(timeout=5)
            raise RuntimeError(
                f"Konuşma modeli beklenmedik biçimde kapandı (çıkış kodu: {process.exitcode})."
            ) from exc
    finally:
        parent_connection.close()

    process.join(timeout=5)
    if process.is_alive():
        process.terminate()
        process.join(timeout=5)
    if not payload.get("ok"):
        raise RuntimeError(payload.get("error") or "Konuşma modeli bilinmeyen bir hata verdi.")
    return payload["result"]


def _run_transcription(path: Path, topic_hint: str) -> dict:
    if settings.is_production:
        return _run_isolated_transcription(path, topic_hint)
    return _transcribe_with_model(_get_model(), path, topic_hint)


@router.post("/transcribe")
async def transcribe_audio(
    audio: UploadFile = File(...),
    topic_hint: str = Form(default="", max_length=600),
    _human=Depends(require_human),
    _rate=Depends(rate_limit_transcribe),
    _slot=Depends(limit_transcribe_concurrency),
):
    content_type = (audio.content_type or "").split(";")[0].lower()
    suffix = _allowed_types.get(content_type)
    if not suffix:
        await audio.close()
        raise HTTPException(415, "Tarayıcının ürettiği ses biçimi desteklenmiyor.")

    max_bytes = settings.max_speaking_audio_mb * 1024 * 1024
    file_descriptor, raw_path = tempfile.mkstemp(prefix="speaking-", suffix=suffix, dir=settings.storage_dir / "transient")
    os.close(file_descriptor)
    path = Path(raw_path)
    total = 0
    try:
        with path.open("wb") as target:
            while chunk := await audio.read(1024 * 1024):
                total += len(chunk)
                if total > max_bytes:
                    raise HTTPException(413, f"Ses kaydı {settings.max_speaking_audio_mb} MB sınırını aşıyor.")
                target.write(chunk)
        if total < 256:
            raise HTTPException(400, "Ses kaydı boş veya çok kısa.")
        try:
            result = await run_in_threadpool(_run_transcription, path, topic_hint)
        except HTTPException:
            raise
        except Exception as exc:  # noqa: BLE001
            raise HTTPException(502, f"Ses yazıya çevrilemedi: {str(exc)[:500]}") from exc
        if not result["text"]:
            raise HTTPException(422, "Kayıtta anlaşılır İngilizce konuşma bulunamadı. Mikrofon girişini kontrol edip tekrar dene.")
        return {**result, "audio_deleted": True}
    finally:
        await audio.close()
        path.unlink(missing_ok=True)
