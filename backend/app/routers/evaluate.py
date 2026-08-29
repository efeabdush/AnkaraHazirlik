from __future__ import annotations

import json
import re

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from ..rate_limit import limit_ai_concurrency, rate_limit_coach, rate_limit_evaluate
from .security import require_human
from ..services.llm import LLMError, active_summary, complete, llm_available, parse_json_object

router = APIRouter(prefix="/api/evaluate", tags=["evaluation"])

WRITING_DIMENSIONS = ("task_completion", "grammar", "vocabulary", "coherence_cohesion")
SPEAKING_DIMENSIONS = ("task_completion", "grammar", "vocabulary", "fluency_pronunciation")


class WritingIn(BaseModel):
    prompt: str = Field(min_length=10, max_length=1200)
    essay: str = Field(min_length=20, max_length=12000)


class SpeakingMetrics(BaseModel):
    duration_sec: int = Field(ge=0, le=3600)
    word_count: int = Field(ge=0, le=10000)
    filler_count: int = Field(ge=0, le=10000)
    repeated_phrases: list[str] = Field(default_factory=list, max_length=20)
    long_pause_count: int = Field(default=0, ge=0, le=1000)
    hesitation_pause_count: int = Field(default=0, ge=0, le=2000)
    word_repetition_count: int = Field(default=0, ge=0, le=2000)
    elongation_count: int = Field(default=0, ge=0, le=2000)
    unclear_word_count: int = Field(default=0, ge=0, le=2000)
    filler_words: dict[str, int] = Field(default_factory=dict)
    speech_rate_wpm: float = Field(default=0, ge=0, le=500)


class SpeakingIn(BaseModel):
    topic: str = Field(min_length=4, max_length=1000)
    transcript: str = Field(min_length=5, max_length=16000)
    metrics: SpeakingMetrics


class ChatMessage(BaseModel):
    role: str
    content: str = Field(min_length=1, max_length=4000)


class CoachIn(BaseModel):
    context: str = Field(min_length=10, max_length=12000)
    messages: list[ChatMessage] = Field(min_length=1, max_length=24)


def _require_llm() -> None:
    if not llm_available() or not active_summary()["ready"]:
        raise HTTPException(503, "Değerlendirme modeli hazır değil. Site sahibi panelden model seçmeli.")


def _safe_json(system: str, user: str) -> dict:
    try:
        return parse_json_object(complete(system, user, json_mode=True))
    except LLMError as exc:
        raise HTTPException(502, str(exc)) from exc


def _rubric_scores(raw: object, dimensions: tuple[str, ...], max_gap: float | None = None) -> dict[str, float]:
    source = raw if isinstance(raw, dict) else {}
    scores: dict[str, float] = {}
    for key in dimensions:
        try:
            value = float(source.get(key, 0))
        except (TypeError, ValueError):
            value = 0
        scores[key] = max(0, min(2.5, round(value * 2) / 2))
    if max_gap is not None:
        floor = min(scores.values())
        scores = {key: min(value, floor + max_gap) for key, value in scores.items()}
    return scores


def _short_strings(raw: object, limit: int, fallback: list[str] | None = None) -> list[str]:
    if not isinstance(raw, list):
        return fallback or []
    items = [str(item).strip()[:500] for item in raw if str(item).strip()]
    return items[:limit] or (fallback or [])


def _normalize_writing(result: dict, word_count: int) -> dict:
    scores = _rubric_scores(result.get("scores"), WRITING_DIMENSIONS, max_gap=1)
    if word_count < 250:
        task_cap = 1.5 if word_count >= 200 else 1.0 if word_count >= 120 else 0.5
        scores["task_completion"] = min(scores["task_completion"], task_cap)
        floor = min(scores.values())
        scores = {key: min(value, floor + 1) for key, value in scores.items()}
    total = round(sum(scores.values()), 1)
    fixes = []
    for item in result.get("sentence_fixes") if isinstance(result.get("sentence_fixes"), list) else []:
        if not isinstance(item, dict):
            continue
        original, improved = str(item.get("original", "")).strip(), str(item.get("improved", "")).strip()
        if original and improved:
            fixes.append({"original": original[:700], "improved": improved[:700], "reason_tr": str(item.get("reason_tr", "")).strip()[:500]})
    return {
        "scores": scores,
        "raw_total_10": total,
        "session_score_20": round(total * 2, 1),
        "word_count": word_count,
        "minimum_met": word_count >= 250,
        "level_summary_tr": str(result.get("level_summary_tr", "Değerlendirme tamamlandı.")).strip()[:700],
        "strengths_tr": _short_strings(result.get("strengths_tr"), 3),
        "priorities_tr": _short_strings(result.get("priorities_tr"), 4, ["Bir sonraki denemede tek bir ölçülebilir hedef seç."]),
        "sentence_fixes": fixes[:4],
        "next_practice_tr": _short_strings(result.get("next_practice_tr"), 3, ["Düzeltmeleri kullanarak bir paragrafı yeniden yaz."]),
        "disclaimer_tr": "Bu çalışma puanı AI tahminidir; Ankara Üniversitesi tarafından verilmiş resmî bir sınav puanı değildir.",
    }


def _normalize_speaking(result: dict, metrics: SpeakingMetrics) -> dict:
    scores = _rubric_scores(result.get("scores"), SPEAKING_DIMENSIONS)
    total = round(sum(scores.values()), 1)
    phrases = []
    for item in result.get("better_phrases") if isinstance(result.get("better_phrases"), list) else []:
        if not isinstance(item, dict):
            continue
        old, new = str(item.get("instead_of", "")).strip(), str(item.get("try", "")).strip()
        if old and new:
            phrases.append({"instead_of": old[:500], "try": new[:500], "why_tr": str(item.get("why_tr", "")).strip()[:500]})
    filler_breakdown = ", ".join(f"{word}: {count}" for word, count in metrics.filler_words.items()) or "ayrıştırılamadı"
    fallback_filler = (
        f"Yaklaşık dolgu sesi: {metrics.filler_count} ({filler_breakdown}); kısa tereddüt duraklaması: "
        f"{metrics.hesitation_pause_count}; kelime tekrarı: {metrics.word_repetition_count}; uzatma: {metrics.elongation_count}. "
        "Otomatik ses analizi kusursuz değildir; bu veriyi eğilim olarak kullan."
    )
    return {
        "scores": scores,
        "raw_total_10": total,
        "session_score_20": round(total * 2, 1),
        "level_summary_tr": str(result.get("level_summary_tr", "Değerlendirme tamamlandı.")).strip()[:700],
        "evidence_tr": _short_strings(result.get("evidence_tr"), 4),
        "priorities_tr": _short_strings(result.get("priorities_tr"), 4, ["Tekrar kaydında bir ana fikri iki somut ayrıntıyla geliştir."]),
        "filler_feedback_tr": str(result.get("filler_feedback_tr", fallback_filler)).strip()[:700] or fallback_filler,
        "better_phrases": phrases[:5],
        "next_drill_tr": _short_strings(result.get("next_drill_tr"), 3, ["Aynı kartı bir kez daha, daha az duraklamayla anlat."]),
        "disclaimer_tr": "Bu çalışma puanı transkript ve yaklaşık konuşma verilerine dayalı bir AI tahminidir; resmî puan değildir ve telaffuzu kesin ölçemez.",
    }


@router.post("/writing")
def evaluate_writing(
    body: WritingIn,
    _human=Depends(require_human),
    _rate=Depends(rate_limit_evaluate),
    _slot=Depends(limit_ai_concurrency),
):
    _require_llm()
    words = re.findall(r"[A-Za-z]+(?:['’-][A-Za-z]+)?", body.essay)
    system = """You are a strict but constructive unofficial practice evaluator using the published Ankara University B1+ proficiency writing criteria.
Use four official-style dimensions: task_completion, grammar, vocabulary, coherence_cohesion.
Each dimension must be one of 0, 0.5, 1, 1.5, 2, 2.5. The maximum gap between dimensions is 1 point.
Judge an opinion essay, not a paragraph or list. Do not inflate scores. B1+ allows understandable errors but expects a clear thesis, developed reasons/examples, some complex structures, adequate range, and logical progression.
Return JSON only with: scores (the four keys), raw_total_10, session_score_20, level_summary_tr, strengths_tr (max 3 short items), priorities_tr (max 4 short items), sentence_fixes (max 4 objects with original, improved, reason_tr), next_practice_tr (max 3 short items), disclaimer_tr.
Write feedback in concise Turkish. Be specific, calm and realistic; never shame or flatter. session_score_20 is raw_total_10 * 2."""
    user = f"Prompt:\n{body.prompt}\n\nWord count: {len(words)}\n\nEssay:\n{body.essay}"
    return _normalize_writing(_safe_json(system, user), len(words))


@router.post("/speaking")
def evaluate_speaking(
    body: SpeakingIn,
    _human=Depends(require_human),
    _rate=Depends(rate_limit_evaluate),
    _slot=Depends(limit_ai_concurrency),
):
    _require_llm()
    system = """You are a strict but constructive unofficial practice evaluator using the published Ankara University B1+ proficiency speaking criteria.
Use four official-style dimensions: task_completion, grammar, vocabulary, fluency_pronunciation.
Each dimension must be one of 0, 0.5, 1, 1.5, 2, 2.5. Do not inflate scores.
The transcript may contain speech-recognition mistakes, so do not pretend to measure exact pronunciation from text. Use duration, word count, filler words, hesitation pauses, word repetitions, elongated fillers, unclear-word count, long pauses, repeated phrases, and speech rate for fluency evidence. Explicitly mention concrete disfluency counts when they are elevated, but describe them as approximate. Mention the limitation clearly.
Return JSON only with: scores, raw_total_10, session_score_20, level_summary_tr, evidence_tr (max 4 short items), priorities_tr (max 4 short items), filler_feedback_tr, better_phrases (max 5 objects with instead_of, try, why_tr), next_drill_tr (max 3 short items), disclaimer_tr.
Feedback must be concise Turkish, stoic, calm, direct and practical. No empty praise. Never say the learner cannot reach B1+. Remind them there is enough time to improve with deliberate practice."""
    user = (
        f"Topic card:\n{body.topic}\n\nMetrics:\n{json.dumps(body.metrics.model_dump(), ensure_ascii=False)}"
        f"\n\nTranscript:\n{body.transcript}"
    )
    return _normalize_speaking(_safe_json(system, user), body.metrics)


@router.post("/coach")
def coach(
    body: CoachIn,
    _human=Depends(require_human),
    _rate=Depends(rate_limit_coach),
    _slot=Depends(limit_ai_concurrency),
):
    _require_llm()
    allowed = [m for m in body.messages if m.role in {"user", "assistant"}]
    if not allowed or allowed[-1].role != "user":
        raise HTTPException(400, "Son mesaj kullanıcı mesajı olmalı.")
    history = "\n".join(f"{m.role.upper()}: {m.content}" for m in allowed)
    system = """You are a Turkish-speaking B1+ English practice coach. You remember and use the conversation history supplied below.
Your tone is stoic, calm, realistic and demanding without demotivating the learner. Do not flatter. Give concrete drills, corrected examples and measurable next actions. Keep replies compact and easy to scan. Use simple Markdown with **bold** labels and short bullet or numbered lists where that improves scanning; never put spaces just inside emphasis markers. If the learner is anxious, state plainly that there is enough time to reach B1+ through consistent deliberate practice, then return to the actionable issue. Never claim to be an official Ankara University evaluator."""
    user = f"Practice context:\n{body.context}\n\nConversation:\n{history}\n\nReply to the final USER message."
    try:
        reply = complete(system, user, json_mode=False).strip()
    except LLMError as exc:
        raise HTTPException(502, str(exc)) from exc
    return {"reply": reply}
