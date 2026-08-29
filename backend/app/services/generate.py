from __future__ import annotations

import json

from sqlalchemy.orm import Session

from ..config import settings
from ..models import GenerationJob, Question, Test
from .llm import complete, parse_json_object
from .glossary import generate_glossary, local_glossary
from .tts import synthesize_script
from .validator import ACADEMIC_KINDS, ValidationError, validate_academic_pack, validate_pack


def _system_prompt() -> str:
    path = settings.content_dir / "prompts" / "generate_system.txt"
    return path.read_text(encoding="utf-8")


def _academic_system_prompt() -> str:
    return (settings.content_dir / "prompts" / "academic_generate_system.txt").read_text(encoding="utf-8")


def run_generation_job(db: Session, job_id: str) -> None:
    job = db.get(GenerationJob, job_id)
    if not job:
        return
    try:
        job.status = "script"
        db.commit()
        if job.kind in ACADEMIC_KINDS:
            _run_academic_generation(db, job)
            return
        user = (
            f"Create a {job.kind} listening pack at B1+.\n"
            f"Topic or request: {job.topic or 'campus or academic everyday life'}\n"
            "Return one JSON object only."
        )
        raw = complete(_system_prompt(), user, json_mode=True)
        data = parse_json_object(raw)
        try:
            data = validate_pack(job.kind, data)
        except ValidationError:
            raw = complete(
                _system_prompt(),
                user + "\nYour previous JSON failed length or question checks. Fix it.",
                json_mode=True,
            )
            data = validate_pack(job.kind, parse_json_object(raw))

        job.status = "glossary"
        db.commit()
        try:
            glossary = generate_glossary(data)
        except Exception as exc:  # noqa: BLE001
            print(f"Glossary skipped: {exc}")
            glossary = local_glossary(data)

        job.status = "audio"
        db.commit()
        test = Test(
            kind=job.kind,
            title=data["title"],
            topic=data.get("topic") or job.topic,
            source="ai",
            published=True,
            transcript_json=json.dumps(data["script"], ensure_ascii=False),
            note_scaffold=json.dumps(data.get("note_scaffold") or [], ensure_ascii=False),
            glossary_json=json.dumps(
                {"entries": glossary.get("entries") or [], "words": glossary.get("words") or {}},
                ensure_ascii=False,
            ),
        )
        db.add(test)
        db.flush()
        points = 1 if job.kind == "conversation" else 2
        for i, q in enumerate(data["questions"], start=1):
            db.add(
                Question(
                    test_id=test.id,
                    order=i,
                    stem=q["stem"],
                    options_json=json.dumps(q["options"], ensure_ascii=False),
                    answer=q["answer"],
                    points=q.get("points", points),
                    rationale=q.get("rationale", ""),
                    qtype=q.get("qtype", "detail"),
                )
            )
        audio_path = settings.storage_dir / "audio" / f"{test.id}.mp3"
        duration = synthesize_script(data["script"], audio_path)
        test.audio_path = str(audio_path)
        test.duration_sec = duration
        job.test_id = test.id
        job.status = "ready"
        db.commit()
    except Exception as exc:  # noqa: BLE001
        db.rollback()
        job = db.get(GenerationJob, job_id)
        if job:
            job.status = "failed"
            job.error = str(exc)[:2000]
            db.commit()


def _run_academic_generation(db: Session, job: GenerationJob) -> None:
    user = (
        f"Create one original {job.kind} practice pack at B1+ level.\n"
        f"Topic or request: {job.topic or 'university life or a familiar general topic'}\n"
        "Return one JSON object only."
    )
    raw = complete(_academic_system_prompt(), user, json_mode=True)
    try:
        data = validate_academic_pack(job.kind, parse_json_object(raw))
    except ValidationError:
        raw = complete(
            _academic_system_prompt(),
            user + "\nThe previous output failed the exact schema or count. Correct it without changing the kind.",
            json_mode=True,
        )
        data = validate_academic_pack(job.kind, parse_json_object(raw))

    test = Test(
        kind=job.kind,
        title=data["title"],
        topic=data.get("topic") or job.topic,
        source="ai",
        published=True,
        content_json=json.dumps(data["content"], ensure_ascii=False),
        instructions=data.get("instructions", ""),
    )
    db.add(test)
    db.flush()
    default_points = 2 if job.kind == "reading_insertion" else 1
    for i, q in enumerate(data.get("questions") or [], start=1):
        db.add(
            Question(
                test_id=test.id,
                order=i,
                stem=q["stem"],
                options_json=json.dumps(q["options"], ensure_ascii=False),
                answer=q["answer"],
                points=q.get("points", default_points),
                rationale=q.get("rationale", ""),
                qtype=q.get("qtype", job.kind),
            )
        )
    job.test_id = test.id
    job.status = "ready"
    db.commit()
