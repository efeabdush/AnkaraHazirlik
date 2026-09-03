from pathlib import Path

from fastapi.testclient import TestClient

from app.config import settings
from app.main import app
from app.routers import transcribe


def _transient_files() -> set[Path]:
    return set((settings.storage_dir / "transient").iterdir())


def test_disfluency_analysis_counts_fillers_repetitions_and_pauses():
    result = transcribe._analyze_disfluencies(
        [
            {"word": "Um", "start": 0.0, "end": 0.9, "probability": 0.9},
            {"word": "I", "start": 1.0, "end": 1.2, "probability": 0.9},
            {"word": "I", "start": 1.3, "end": 1.5, "probability": 0.9},
            {"word": "think", "start": 2.1, "end": 2.5, "probability": 0.2},
            {"word": "hmm", "start": 2.7, "end": 3.6, "probability": 0.8},
        ]
    )

    assert result["filler_count"] == 2
    assert result["word_repetition_count"] == 1
    assert result["hesitation_pause_count"] == 1
    assert result["elongation_count"] == 2
    assert result["unclear_word_count"] == 1


def test_production_builds_a_fresh_transcription_model(monkeypatch):
    models = iter([object(), object()])
    monkeypatch.setattr(settings, "railway_environment", "production")
    monkeypatch.setattr(transcribe, "_build_model", lambda: next(models))

    first = transcribe._get_model()
    second = transcribe._get_model()

    assert first is not second
    assert transcribe._model is None


def test_production_transcription_uses_disposable_worker(monkeypatch, tmp_path):
    expected = {"text": "isolated result"}
    monkeypatch.setattr(settings, "railway_environment", "production")
    monkeypatch.setattr(transcribe, "_run_isolated_transcription", lambda path, topic: expected)
    monkeypatch.setattr(
        transcribe,
        "_get_model",
        lambda: (_ for _ in ()).throw(AssertionError("model must not load in the web process")),
    )

    assert transcribe._run_transcription(tmp_path / "answer.webm", "education") == expected


def test_transcribe_returns_text_and_deletes_temporary_audio(monkeypatch):
    before = _transient_files()
    monkeypatch.setattr(
        transcribe,
        "_run_transcription",
        lambda path, topic: {
            "text": "This is a complete speaking answer.",
            "language": "en",
            "language_probability": 0.99,
            "duration_sec": 8,
            "speech_duration_sec": 7,
            "long_pause_count": 1,
            "segments": [],
        },
    )

    with TestClient(app) as client:
        response = client.post(
            "/api/transcribe",
            files={"audio": ("answer.webm", b"a" * 512, "audio/webm")},
            data={"topic_hint": "education"},
        )

    assert response.status_code == 200
    assert response.json()["text"] == "This is a complete speaking answer."
    assert response.json()["audio_deleted"] is True
    assert _transient_files() == before


def test_transcribe_deletes_temporary_audio_after_failure(monkeypatch):
    before = _transient_files()

    def fail(_path, _topic):
        raise RuntimeError("model failure")

    monkeypatch.setattr(transcribe, "_run_transcription", fail)
    with TestClient(app) as client:
        response = client.post(
            "/api/transcribe",
            files={"audio": ("answer.webm", b"a" * 512, "audio/webm")},
        )

    assert response.status_code == 502
    assert _transient_files() == before
