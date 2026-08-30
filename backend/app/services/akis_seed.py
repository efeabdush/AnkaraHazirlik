from __future__ import annotations

import json
import shutil
from datetime import datetime, timedelta
from pathlib import Path

from sqlalchemy.orm import Session

from ..config import settings
from ..models import AkisReel
from .tts import estimate_seconds, synthesize_script

SEED_EPOCH = datetime(2026, 1, 1)


def _files() -> list[Path]:
    return sorted((settings.content_dir / "akis" / "reels").glob("*.json"))


def seed_akis(db: Session) -> None:
    """Load every missing Akış card without replacing learner-facing data."""
    position = 0
    for path in _files():
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"Akış seed skipped {path.name}: {exc}")
            continue
        cards = payload if isinstance(payload, list) else [payload]
        for card in cards:
            try:
                _load(db, card, position)
                db.commit()
            except Exception as exc:  # noqa: BLE001
                db.rollback()
                print(f"Akış seed skipped {path.name} #{position}: {exc}")
            position += 1


def _load(db: Session, data: dict, position: int) -> AkisReel:
    question = data["question"]
    kind = str(data.get("kind") or "sorular")
    reel = db.get(AkisReel, data["id"])
    if reel is None:
        reel = AkisReel(
            id=data["id"],
            kind=kind,
            level=data.get("level", "A2"),
            title=data["title"],
            topic=data.get("topic", ""),
            body=data.get("body", ""),
            script_json=json.dumps(data.get("script") or [], ensure_ascii=False),
            stem=question["stem"],
            options_json=json.dumps(question["options"], ensure_ascii=False),
            answer=question["answer"],
            explain_tr=question.get("explain_tr", ""),
            key_line=question.get("key_line") or question.get("correct_form") or "",
            seconds=estimate_seconds(data.get("script") or [], data.get("level", "A2")) if kind == "sorular" else 0,
            source="seed",
            published=data.get("published", True),
        )
        db.add(reel)
        db.flush()
    reel.created_at = SEED_EPOCH + timedelta(seconds=position)
    if kind != "sorular":
        return reel

    audio_path = settings.storage_dir / "audio" / "akis" / f"{reel.id}.mp3"
    bundled = settings.content_dir / "akis" / "audio" / f"{reel.id}.mp3"
    audio_path.parent.mkdir(parents=True, exist_ok=True)
    if not audio_path.exists() and bundled.exists():
        shutil.copyfile(bundled, audio_path)
    if not audio_path.exists():
        try:
            reel.seconds = synthesize_script(data["script"], audio_path, reel.level)
        except Exception as exc:  # noqa: BLE001
            print(f"Akış TTS skipped for {reel.id}: {exc}")
    if audio_path.exists():
        reel.audio_path = str(audio_path)
    return reel
