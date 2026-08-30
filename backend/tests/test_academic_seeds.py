import json
from pathlib import Path

import pytest

from app.services.practice_catalog import build_practice_catalog
from app.services.validator import validate_academic_pack, validate_pack


SEED_DIR = Path(__file__).resolve().parents[2] / "content" / "seeds"
ACADEMIC = {
    "reading_standard": (25, 1),
    "reading_insertion": (25, 2),
    "cloze": (25, 1),
    "restatement": (25, 1),
    "writing_prompt": (4, None),
    "speaking_card": (100, None),
}


def _seed_packs(kind: str) -> list[dict]:
    packs = []
    for path in SEED_DIR.glob("*.json"):
        if path.name.endswith(".glossary.json"):
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("kind") == kind:
            packs.append(data)
    return packs


def _packs(kind: str) -> list[dict]:
    return _seed_packs(kind) + [pack for pack in build_practice_catalog() if pack["kind"] == kind]


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
        for pack in _seed_packs(kind):
            total += sum(question["points"] for question in pack["questions"])
    assert total == 40


def test_clean_install_has_twenty_five_valid_tracks_per_listening_kind():
    conversations = _packs("conversation")
    lectures = _packs("lecture")
    assert len(conversations) == 25
    assert len(lectures) == 25
    for pack in conversations:
        validate_pack("conversation", pack)
        assert sum(question.get("points", 1) for question in pack["questions"]) == 4
    for pack in lectures:
        validate_pack("lecture", pack)
        assert sum(question.get("points", 2) for question in pack["questions"]) == 8


def test_speaking_catalog_has_one_hundred_unique_cards():
    cards = _packs("speaking_card")
    assert len({card["id"] for card in cards}) == 100
    assert len({card["title"] for card in cards}) == 100
    assert len({card["content"]["prompt"] for card in cards}) == 100
