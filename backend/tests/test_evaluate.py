from app.routers.evaluate import (
    SPEAKING_EVALUATOR_SYSTEM,
    SpeakingMetrics,
    _normalize_speaking,
    _normalize_writing,
)


def test_writing_normalizer_enforces_word_limit_and_rubric_steps():
    raw = {
        "scores": {"task_completion": 2.5, "grammar": 2.3, "vocabulary": 9, "coherence_cohesion": 2.5},
        "level_summary_tr": "Strong",
        "priorities_tr": ["Improve examples"],
    }
    result = _normalize_writing(raw, 239)
    assert result["minimum_met"] is False
    assert result["scores"]["task_completion"] <= 1.5
    assert max(result["scores"].values()) - min(result["scores"].values()) <= 1
    assert result["raw_total_10"] == sum(result["scores"].values())
    assert "resmî" in result["disclaimer_tr"]


def test_speaking_normalizer_recomputes_total_and_disclaimer():
    metrics = SpeakingMetrics(duration_sec=90, word_count=120, filler_count=4, repeated_phrases=[])
    raw = {"scores": {"task_completion": 2.4, "grammar": -1, "vocabulary": "2", "fluency_pronunciation": 1.6}}
    result = _normalize_speaking(raw, metrics)
    assert result["scores"] == {"task_completion": 2.5, "grammar": 0, "vocabulary": 2, "fluency_pronunciation": 1.5}
    assert result["session_score_20"] == 12
    assert "telaffuzu kesin ölçemez" in result["disclaimer_tr"]


def test_speaking_normalizer_allows_the_full_score_range():
    metrics = SpeakingMetrics(duration_sec=90, word_count=150, filler_count=0)
    raw = {
        "scores": {
            "task_completion": 2.5,
            "grammar": 2.5,
            "vocabulary": 2.5,
            "fluency_pronunciation": 2.5,
        }
    }
    result = _normalize_speaking(raw, metrics)
    assert result["raw_total_10"] == 10
    assert result["session_score_20"] == 20


def test_speaking_prompt_handles_probable_transcription_artifacts_conservatively():
    assert '"C onsist ent is the K"' in SPEAKING_EVALUATOR_SYSTEM
    assert 'probably "Consistency is the key"' in SPEAKING_EVALUATOR_SYSTEM
    assert "do not cluster routine answers around 1.5 or 2" in SPEAKING_EVALUATOR_SYSTEM
    assert "exclude that fragment from grammar and vocabulary penalties" in SPEAKING_EVALUATOR_SYSTEM
    assert "does not automatically lower the learner's language score" in SPEAKING_EVALUATOR_SYSTEM
