from app.routers.evaluate import SpeakingMetrics, _normalize_speaking, _normalize_writing


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
