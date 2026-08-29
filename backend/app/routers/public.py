from __future__ import annotations

import json

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..config import settings
from ..db import get_db
from ..models import Attempt, Test
from ..services.glossary import merge_entries, word_bank_for

router = APIRouter(prefix="/api", tags=["public"])


def _glossary_pack(raw: str | None) -> tuple[list, dict]:
    try:
        data = json.loads(raw or "[]")
    except json.JSONDecodeError:
        return [], {}
    if isinstance(data, dict):
        entries = data.get("entries") or []
        words = data.get("words") or {}
    else:
        entries, words = data, {}
    return (
        entries if isinstance(entries, list) else [],
        words if isinstance(words, dict) else {},
    )


def _seed_glossary_from_disk(test_id: str) -> tuple[list, dict]:
    """If DB was created before Turkish packs existed, read the seed file live."""
    seed_dir = settings.content_dir / "seeds"
    for path in seed_dir.glob("*.json"):
        if path.name.endswith(".glossary.json"):
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if data.get("id") != test_id:
            continue
        raw = data.get("glossary")
        if raw is None:
            gpath = path.with_name(path.stem + ".glossary.json")
            if not gpath.exists():
                return [], {}
            try:
                raw = json.loads(gpath.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                return [], {}
        if isinstance(raw, dict):
            return (
                merge_entries(raw.get("entries") or []),
                raw.get("words") if isinstance(raw.get("words"), dict) else {},
            )
        if isinstance(raw, list):
            return merge_entries(raw), {}
    return [], {}


def _study_aids(t: Test, db: Session | None = None) -> dict:
    """Precomputed Turkish for selections: sentences/phrases plus a word bank."""
    entries, pack_words = _glossary_pack(t.glossary_json)
    if not entries:
        disk_entries, disk_words = _seed_glossary_from_disk(t.id)
        if disk_entries or disk_words:
            entries = disk_entries
            pack_words = {**disk_words, **pack_words}
            t.glossary_json = json.dumps(
                {"entries": entries, "words": pack_words},
                ensure_ascii=False,
            )
            if db is not None:
                try:
                    db.commit()
                except Exception:  # noqa: BLE001
                    db.rollback()
    pack = {
        "title": t.title,
        "script": json.loads(t.transcript_json or "[]"),
        "content": json.loads(t.content_json or "{}"),
        "questions": [
            {
                "stem": q.stem,
                "options": json.loads(q.options_json),
                "rationale": q.rationale,
            }
            for q in t.questions
        ],
    }
    return {"glossary": entries, "words": word_bank_for(pack, pack_words)}


class AttemptIn(BaseModel):
    test_id: str
    mode: str = "exam"
    answers: dict[str, str]
    notes: str = ""
    plays_used: int = 0


def _public_test(t: Test, include_questions: bool, hide_answers: bool) -> dict:
    payload = {
        "id": t.id,
        "kind": t.kind,
        "title": t.title,
        "topic": t.topic,
        "cefr": t.cefr,
        "duration_sec": t.duration_sec,
        "source": t.source,
        "instructions": t.instructions,
    }
    if include_questions:
        try:
            payload["content"] = json.loads(t.content_json or "{}")
        except json.JSONDecodeError:
            payload["content"] = {}
        payload["questions"] = [
            {
                "id": q.id,
                "order": q.order,
                "stem": q.stem,
                "options": json.loads(q.options_json),
                "points": q.points,
                **({} if hide_answers else {"answer": q.answer, "rationale": q.rationale}),
            }
            for q in t.questions
        ]
    return payload


@router.get("/tests")
def list_tests(kind: str | None = None, db: Session = Depends(get_db)):
    q = db.query(Test).filter(Test.published.is_(True))
    if kind:
        q = q.filter(Test.kind == kind)
    tests = q.order_by(Test.created_at.asc()).all()
    return [_public_test(t, include_questions=False, hide_answers=True) for t in tests]


@router.get("/tests/{test_id}")
def get_test(test_id: str, db: Session = Depends(get_db)):
    t = db.get(Test, test_id)
    if not t or not t.published:
        raise HTTPException(404, "Test bulunamadı")
    return _public_test(t, include_questions=True, hide_answers=True)


@router.get("/audio/{test_id}")
def get_audio(test_id: str, db: Session = Depends(get_db)):
    from fastapi.responses import FileResponse

    t = db.get(Test, test_id)
    if not t or not t.published or not t.audio_path:
        raise HTTPException(404, "Ses bulunamadı")
    return FileResponse(t.audio_path, media_type="audio/mpeg", filename=f"{test_id}.mp3")


@router.post("/attempts")
def create_attempt(body: AttemptIn, db: Session = Depends(get_db)):
    t = db.get(Test, body.test_id)
    if not t or not t.published:
        raise HTTPException(404, "Test bulunamadı")
    score = 0
    max_score = 0
    details = []
    for q in t.questions:
        max_score += q.points
        chosen = (body.answers.get(q.id) or "").upper()
        ok = chosen == q.answer
        if ok:
            score += q.points
        details.append(
            {
                "id": q.id,
                "order": q.order,
                "stem": q.stem,
                "options": json.loads(q.options_json),
                "points": q.points,
                "chosen": chosen,
                "answer": q.answer,
                "correct": ok,
                "rationale": q.rationale,
            }
        )
    attempt = Attempt(
        test_id=t.id,
        mode=body.mode,
        answers_json=json.dumps(body.answers, ensure_ascii=False),
        notes_text=body.notes,
        score=score,
        max_score=max_score,
        plays_used=body.plays_used,
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return {
        "id": attempt.id,
        "test_id": t.id,
        "kind": t.kind,
        "title": t.title,
        "mode": attempt.mode,
        "score": score,
        "max_score": max_score,
        "notes": attempt.notes_text,
        "content": json.loads(t.content_json or "{}"),
        "transcript": json.loads(t.transcript_json),
        "note_scaffold": t.note_scaffold,
        **_study_aids(t, db),
        "questions": details,
    }


@router.get("/attempts/{attempt_id}")
def get_attempt(attempt_id: str, db: Session = Depends(get_db)):
    a = db.get(Attempt, attempt_id)
    if not a:
        raise HTTPException(404, "Deneme bulunamadı")
    t = a.test
    answers = json.loads(a.answers_json)
    details = []
    for q in t.questions:
        chosen = (answers.get(q.id) or "").upper()
        details.append(
            {
                "id": q.id,
                "order": q.order,
                "stem": q.stem,
                "options": json.loads(q.options_json),
                "points": q.points,
                "chosen": chosen,
                "answer": q.answer,
                "correct": chosen == q.answer,
                "rationale": q.rationale,
            }
        )
    return {
        "id": a.id,
        "test_id": t.id,
        "kind": t.kind,
        "title": t.title,
        "mode": a.mode,
        "score": a.score,
        "max_score": a.max_score,
        "notes": a.notes_text,
        "content": json.loads(t.content_json or "{}"),
        "transcript": json.loads(t.transcript_json),
        "note_scaffold": t.note_scaffold,
        **_study_aids(t, db),
        "questions": details,
    }
