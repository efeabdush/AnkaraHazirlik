from __future__ import annotations

import json
from pathlib import Path

from sqlalchemy.orm import Session

from ..config import settings
from ..models import Question, Test
from .glossary import merge_entries
from .practice_catalog import build_practice_catalog
from .tts import synthesize_script
from .validator import ACADEMIC_KINDS, validate_academic_pack, validate_pack


def seed_if_empty(db: Session) -> None:
    # Seed files are idempotent. Loading missing files on every startup lets us
    # add new practice sections without replacing an existing local database.
    seed_dir = settings.content_dir / "seeds"
    for path in sorted(seed_dir.glob("*.json")):
        if path.name.endswith(".glossary.json"):
            continue
        load_seed_file(db, path)
    for data in build_practice_catalog():
        load_seed_data(db, data)
    db.commit()
    backfill_seed_glossaries(db)


def backfill_seed_glossaries(db: Session) -> None:
    seed_dir = settings.content_dir / "seeds"
    for path in sorted(seed_dir.glob("*.json")):
        if path.name.endswith(".glossary.json"):
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        test = db.get(Test, data.get("id"))
        if not test:
            continue
        built = _glossary_for_seed(path, data)
        if not built["entries"] and not built["words"]:
            continue
        if built != _stored_glossary(test):
            test.glossary_json = json.dumps(built, ensure_ascii=False)
    db.commit()


def _stored_glossary(test: Test) -> dict:
    try:
        data = json.loads(test.glossary_json or "[]")
    except json.JSONDecodeError:
        return {"entries": [], "words": {}}
    if isinstance(data, dict):
        return {"entries": data.get("entries") or [], "words": data.get("words") or {}}
    return {"entries": data if isinstance(data, list) else [], "words": {}}


def _glossary_for_seed(path: Path | None, data: dict) -> dict:
    raw = data.get("glossary")
    if raw is None and path is not None:
        gpath = path.with_name(path.stem + ".glossary.json")
        raw = json.loads(gpath.read_text(encoding="utf-8")) if gpath.exists() else []
    if raw is None:
        raw = []
    if isinstance(raw, dict):
        entries = raw.get("entries") or []
        words = raw.get("words") or {}
    else:
        entries, words = raw, {}
    return {
        "entries": merge_entries(entries if isinstance(entries, list) else []),
        "words": words if isinstance(words, dict) else {},
    }


def load_seed_file(db: Session, path: Path) -> Test:
    data = json.loads(path.read_text(encoding="utf-8"))
    return load_seed_data(db, data, path)


def load_seed_data(db: Session, data: dict, path: Path | None = None) -> Test:
    if data["kind"] in {"conversation", "lecture"}:
        validate_pack(data["kind"], data)
    elif data["kind"] in ACADEMIC_KINDS:
        validate_academic_pack(data["kind"], data)
    existing = db.get(Test, data["id"])
    if existing:
        if existing.source != "seed":
            return existing
        script_json = json.dumps(data.get("script") or [], ensure_ascii=False)
        script_changed = existing.transcript_json != script_json
        existing.kind = data["kind"]
        existing.title = data["title"]
        existing.topic = data.get("topic", "")
        existing.cefr = data.get("cefr", "B1+")
        existing.published = data.get("published", True)
        existing.transcript_json = script_json
        existing.content_json = json.dumps(data.get("content") or {}, ensure_ascii=False)
        existing.instructions = data.get("instructions", "")
        existing.note_scaffold = json.dumps(data.get("note_scaffold") or [], ensure_ascii=False) if not isinstance(data.get("note_scaffold"), str) else data.get("note_scaffold") or ""
        current = sorted(existing.questions, key=lambda question: question.order)
        incoming = data["questions"]
        for i, q in enumerate(incoming, start=1):
            if i <= len(current):
                question = current[i - 1]
                question.order = i
                question.stem = q["stem"]
                question.options_json = json.dumps(q["options"], ensure_ascii=False)
                question.answer = q["answer"]
                question.points = q.get("points", 1 if data["kind"] == "conversation" else 2)
                question.rationale = q.get("rationale", "")
                question.qtype = q.get("qtype", "detail")
            else:
                db.add(Question(test_id=existing.id, order=i, stem=q["stem"], options_json=json.dumps(q["options"], ensure_ascii=False), answer=q["answer"], points=q.get("points", 1 if data["kind"] == "conversation" else 2), rationale=q.get("rationale", ""), qtype=q.get("qtype", "detail")))
        for question in current[len(incoming):]:
            db.delete(question)
        if data["kind"] in {"conversation", "lecture"}:
            audio_path = settings.storage_dir / "audio" / f"{existing.id}.mp3"
            words = sum(len(line["text"].split()) for line in data["script"])
            existing.duration_sec = max(30, int(words / 2.3))
            if not data.get("defer_audio", False):
                if script_changed or not audio_path.exists():
                    try:
                        existing.duration_sec = synthesize_script(data["script"], audio_path)
                    except Exception as exc:  # noqa: BLE001
                        print(f"TTS refresh skipped for {existing.id}: {exc}")
                if audio_path.exists():
                    existing.audio_path = str(audio_path)
            elif audio_path.exists():
                existing.audio_path = str(audio_path)
        existing.glossary_json = json.dumps(_glossary_for_seed(path, data), ensure_ascii=False)
        return existing
    test = Test(
        id=data["id"],
        kind=data["kind"],
        title=data["title"],
        topic=data.get("topic", ""),
        cefr=data.get("cefr", "B1+"),
        source=data.get("source", "seed"),
        published=data.get("published", True),
        transcript_json=json.dumps(data.get("script") or [], ensure_ascii=False),
        content_json=json.dumps(data.get("content") or {}, ensure_ascii=False),
        instructions=data.get("instructions", ""),
        note_scaffold=json.dumps(data.get("note_scaffold") or [], ensure_ascii=False)
        if not isinstance(data.get("note_scaffold"), str)
        else data.get("note_scaffold") or "",
        duration_sec=0,
    )
    db.add(test)
    db.flush()
    for i, q in enumerate(data["questions"], start=1):
        db.add(
            Question(
                test_id=test.id,
                order=i,
                stem=q["stem"],
                options_json=json.dumps(q["options"], ensure_ascii=False),
                answer=q["answer"],
                points=q.get("points", 1 if data["kind"] == "conversation" else 2),
                rationale=q.get("rationale", ""),
                qtype=q.get("qtype", "detail"),
            )
        )
    if data["kind"] in {"conversation", "lecture"}:
        audio_path = settings.storage_dir / "audio" / f"{test.id}.mp3"
        words = sum(len(line["text"].split()) for line in data["script"])
        test.duration_sec = max(30, int(words / 2.3))
        if data.get("defer_audio", False):
            if audio_path.exists():
                test.audio_path = str(audio_path)
        elif not audio_path.exists():
            try:
                duration = synthesize_script(data["script"], audio_path)
                test.duration_sec = duration
                test.audio_path = str(audio_path)
            except Exception as exc:  # noqa: BLE001
                print(f"TTS skipped for {test.id}: {exc}")
        else:
            test.audio_path = str(audio_path)
    test.glossary_json = json.dumps(_glossary_for_seed(path, data), ensure_ascii=False)
    return test
