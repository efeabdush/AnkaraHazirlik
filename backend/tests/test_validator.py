import pytest

from app.services.validator import ValidationError, validate_academic_pack, validate_pack


def test_rejects_wrong_question_count():
    data = {
        "title": "t",
        "topic": "campus",
        "script": [{"speaker": "student", "text": "hello " * 40}] * 6,
        "questions": [],
    }
    try:
        validate_pack("conversation", data)
        assert False
    except ValidationError:
        pass


def test_accepts_minimal_conversation():
    q = {
        "stem": "Why does the student come?",
        "options": {"A": "card problem", "B": "food", "C": "sport", "D": "travel"},
        "answer": "A",
        "qtype": "purpose",
        "rationale": "card",
    }
    script = [{"speaker": "student" if i % 2 == 0 else "staff", "text": "The laundry card problem needs a receipt today. " * 5} for i in range(8)]
    data = {"title": "Laundry", "topic": "campus", "script": script, "questions": [q, q, q, q]}
    out = validate_pack("conversation", data)
    assert out["title"] == "Laundry"


def test_accepts_reading_pack_with_six_questions():
    question = {"stem": "What is stated?", "options": {"A": "One", "B": "Two", "C": "Three", "D": "Four"}, "answer": "A"}
    data = {"title": "Reading", "content": {"paragraphs": ["word " * 400]}, "questions": [question.copy() for _ in range(6)]}
    assert validate_academic_pack("reading_standard", data)["title"] == "Reading"


def test_rejects_incomplete_speaking_card():
    data = {"title": "Speaking", "content": {"bullets": ["one"], "followups": ["one?", "two?"]}, "questions": []}
    with pytest.raises(ValidationError):
        validate_academic_pack("speaking_card", data)
