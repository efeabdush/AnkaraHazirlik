import json
from pathlib import Path

import pytest

from app.services.glossary import (
    local_glossary,
    lookup,
    missing_words,
    pack_words,
    word_bank_for,
)
from app.services.llm import parse_json_object

SEEDS = Path(__file__).resolve().parents[2] / "content" / "seeds"
PACKS = ["conversation_laundry", "lecture_sleep"]


def load(name: str) -> tuple[dict, list, dict]:
    pack = json.loads((SEEDS / f"{name}.json").read_text(encoding="utf-8"))
    raw = json.loads((SEEDS / f"{name}.glossary.json").read_text(encoding="utf-8"))
    if isinstance(raw, dict):
        return pack, raw.get("entries") or [], raw.get("words") or {}
    return pack, raw, {}


@pytest.mark.parametrize("name", PACKS)
def test_every_word_resolves_alone(name):
    pack, entries, words = load(name)
    bank = word_bank_for(pack, words)
    unresolved = [w for w in pack_words(pack) if not lookup(entries, w, bank)]
    assert not unresolved, unresolved


@pytest.mark.parametrize("name", PACKS)
def test_no_missing_dictionary_words(name):
    pack, _entries, words = load(name)
    assert missing_words(pack, words) == []


@pytest.mark.parametrize("name", PACKS)
def test_sentences_and_options_resolve(name):
    pack, entries, words = load(name)
    bank = word_bank_for(pack, words)
    missing = []
    for line in pack["script"]:
        if not lookup(entries, line["text"], bank):
            missing.append(line["text"][:60])
    for q in pack["questions"]:
        for text in [q["stem"], q.get("rationale", ""), *q["options"].values()]:
            if text and not lookup(entries, text, bank):
                missing.append(text[:60])
    assert not missing, missing


def test_single_word_never_returns_a_sentence():
    pack, entries, words = load("conversation_laundry")
    bank = word_bank_for(pack, words)
    for word in ["bother", "receipt", "washing", "coins", "relink"]:
        hit = lookup(entries, word, bank)
        assert hit and hit["kind"] in {"word", "phrase"}, (word, hit)
        assert len(hit["tr"].split()) <= 8


def test_phrase_selection_prefers_the_phrase():
    pack, entries, words = load("lecture_sleep")
    bank = word_bank_for(pack, words)
    assert lookup(entries, "REM sleep", bank)["tr"] == "REM uykusu"
    assert lookup(entries, "long-term memory", bank)["tr"] == "uzun süreli bellek"
    assert lookup(entries, "more important", bank)["tr"] == "daha önemli"


def test_unknown_word_group_falls_back_word_by_word():
    pack, entries, words = load("lecture_sleep")
    bank = word_bank_for(pack, words)
    hit = lookup(entries, "students sleep badly", bank)
    assert hit["kind"] == "words"
    assert [p["en"] for p in hit["parts"]] == ["students", "sleep", "badly"]


def test_full_sentence_still_reads_as_one_translation():
    pack, entries, words = load("conversation_laundry")
    bank = word_bank_for(pack, words)
    stem = pack["questions"][0]["stem"]
    hit = lookup(entries, stem, bank)
    assert hit["kind"] in {"phrase", "sentence"}
    assert "ilk sorunu" in hit["tr"].lower()


def test_curly_apostrophe_and_trailing_punctuation():
    entries = [{"en": "What is the student's first problem?", "tr": "Öğrencinin ilk sorunu nedir?"}]
    assert lookup(entries, "What is the student’s first problem?", {})["tr"].startswith("Öğrencinin")
    assert lookup([], "lecture.", {"lecture": "ders"})["tr"] == "ders"


def test_plural_and_tense_forms_use_the_base_word():
    bank = {"turnstile": "turnike", "enrol": "kaydolmak", "supervise": "denetlemek"}
    assert lookup([], "turnstiles", bank)["tr"] == "turnike"
    assert lookup([], "enrolled", bank)["tr"] == "kaydolmak"
    assert lookup([], "supervising", bank)["tr"] == "denetlemek"


def test_local_glossary_covers_seed_words_without_llm():
    pack, _entries, _words = load("lecture_sleep")
    built = local_glossary(pack)
    assert built["entries"] == []
    assert len(built["words"]) > 100
    for word in ["sleep", "lecture", "memory", "student", "because"]:
        assert lookup([], word, built["words"])


def test_parse_json_object_strips_fences_and_noise():
    data = parse_json_object('here you go\n```json\n{"words":{"sleep":"uyku"}}\n```\nthanks')
    assert data["words"]["sleep"] == "uyku"
