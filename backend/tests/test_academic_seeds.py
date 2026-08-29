import json
from pathlib import Path

import pytest

from app.services.validator import validate_academic_pack, validate_pack


SEED_DIR = Path(__file__).resolve().parents[2] / "content" / "seeds"
ACADEMIC = {
    "reading_standard": (2, 1),
    "reading_insertion": (1, 2),
    "cloze": (3, 1),
    "restatement": (1, 1),
    "writing_prompt": (4, None),
    "speaking_card": (8, None),
}


def _packs(kind: str) -> list[dict]:
    packs = []
    for path in SEED_DIR.glob("*.json"):
        if path.name.endswith(".glossary.json"):
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("kind") == kind:
            packs.append(data)
    return packs


@pytest.mark.parametrize("kind", ACADEMIC)
def test_every_academic_seed_matches_its_schema(kind: str):
    expected_count, points = ACADEMIC[kind]
    packs = _packs(kind)
    assert len(packs) == expected_count
    for pack in packs:
        validate_academic_pack(kind, pack)
        if points is not None:
            assert {question["points"] for question in pack["questions"]} == {points}


def test_session_one_academic_score_is_exactly_forty():
    total = 0
    for kind in ("reading_standard", "reading_insertion", "cloze", "restatement"):
        for pack in _packs(kind):
            total += sum(question["points"] for question in pack["questions"])
    assert total == 40


def test_clean_install_has_three_valid_conversation_tracks_and_one_lecture():
    conversations = _packs("conversation")
    lectures = _packs("lecture")
    assert len(conversations) == 3
    assert len(lectures) == 1
    for pack in conversations:
        validate_pack("conversation", pack)
        assert sum(question.get("points", 1) for question in pack["questions"]) == 4
    validate_pack("lecture", lectures[0])
    assert sum(question.get("points", 2) for question in lectures[0]["questions"]) == 8
