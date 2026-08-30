from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..config import settings
from ..db import get_db
from ..models import AKIS_KINDS, AKIS_LEVELS, AkisReel
from ..rate_limit import limit_ai_concurrency, rate_limit_akis_chat
from ..services.llm import LLMError, active_summary, chat as llm_chat, llm_available
from .security import require_human

router = APIRouter(prefix="/api/akis", tags=["akis"])
LEVEL_ORDER = {"A1": 0, "A2": 1, "B1": 2, "B1+": 3}


def _kind(value: str | None) -> str:
    picked = (value or "sorular").strip().lower()
    if picked not in AKIS_KINDS:
        raise HTTPException(404, "Bilinmeyen biçim")
    return picked


def _level_cards(db: Session, kind: str, level: str) -> list[AkisReel]:
    return (
        db.query(AkisReel)
        .filter(AkisReel.published.is_(True), AkisReel.kind == kind, AkisReel.level == level)
        .order_by(AkisReel.created_at.asc(), AkisReel.id.asc())
        .all()
    )


def _pack_count(total: int) -> int:
    size = max(1, settings.akis_pack_size)
    return (total + size - 1) // size


def _parse_pack(pack_id: str) -> tuple[str, int]:
    level, _, number = pack_id.rpartition("-")
    if level not in AKIS_LEVELS or not number.isdigit() or int(number) < 1:
        raise HTTPException(404, "Paket bulunamadı")
    return level, int(number)


def _card(reel: AkisReel) -> dict:
    return {
        "id": reel.id,
        "kind": reel.kind,
        "level": reel.level,
        "title": reel.title,
        "topic": reel.topic,
        "seconds": reel.seconds,
        "body": reel.body,
        "stem": reel.stem,
        "options": json.loads(reel.options_json or "{}"),
    }


@router.get("/levels")
def levels(kind: str | None = None, db: Session = Depends(get_db)):
    picked = _kind(kind)
    return [
        {
            "kind": picked,
            "level": level,
            "cards": (total := len(_level_cards(db, picked, level))),
            "packs": _pack_count(total),
            "pack_size": settings.akis_pack_size,
        }
        for level in AKIS_LEVELS
    ]


@router.get("/packs")
def packs(level: str, kind: str | None = None, db: Session = Depends(get_db)):
    picked = _kind(kind)
    level = level.strip().upper()
    if level not in AKIS_LEVELS:
        raise HTTPException(404, "Seviye bulunamadı")
    cards = _level_cards(db, picked, level)
    size = max(1, settings.akis_pack_size)
    result = []
    for index in range(_pack_count(len(cards))):
        chunk = cards[index * size : (index + 1) * size]
        result.append(
            {
                "id": f"{level}-{index + 1}",
                "kind": picked,
                "level": level,
                "index": index + 1,
                "title": f"{index + 1}. {level} Paketi",
                "size": len(chunk),
                "pack_size": size,
                "full": len(chunk) == size,
            }
        )
    return {"kind": picked, "level": level, "pack_size": size, "packs": result}


@router.get("/reels")
def reels(
    kind: str | None = None,
    levels: str | None = None,
    pack: str | None = None,
    limit: int = 30,
    shuffle: bool = True,
    db: Session = Depends(get_db),
):
    picked = _kind(kind)
    if pack:
        level, number = _parse_pack(pack)
        cards = _level_cards(db, picked, level)
        size = max(1, settings.akis_pack_size)
        chunk = cards[(number - 1) * size : number * size]
        if not chunk:
            raise HTTPException(404, "Paket bulunamadı")
        return [_card(reel) for reel in chunk]
    query = db.query(AkisReel).filter(AkisReel.published.is_(True), AkisReel.kind == picked)
    wanted = [item.strip().upper() for item in (levels or "").split(",") if item.strip()]
    if wanted:
        query = query.filter(AkisReel.level.in_(wanted))
    cards = query.all()
    if shuffle:
        random.shuffle(cards)
        cards.sort(key=lambda reel: LEVEL_ORDER.get(reel.level, 9))
    else:
        cards.sort(key=lambda reel: (LEVEL_ORDER.get(reel.level, 9), reel.created_at))
    return [_card(reel) for reel in cards[: max(1, min(limit, 100))]]


@router.get("/reels/{reel_id}")
def reel(reel_id: str, db: Session = Depends(get_db)):
    found = db.get(AkisReel, reel_id)
    if not found or not found.published:
        raise HTTPException(404, "Kart bulunamadı")
    return _card(found)


class AnswerIn(BaseModel):
    choice: str = Field(min_length=1, max_length=1)


@router.post("/reels/{reel_id}/answer")
def answer(reel_id: str, body: AnswerIn, db: Session = Depends(get_db)):
    found = db.get(AkisReel, reel_id)
    if not found or not found.published:
        raise HTTPException(404, "Kart bulunamadı")
    options = json.loads(found.options_json or "{}")
    chosen = body.choice.strip().upper()
    if chosen not in options:
        raise HTTPException(400, "Geçersiz şık")
    return {
        "id": found.id,
        "kind": found.kind,
        "chosen": chosen,
        "answer": found.answer,
        "correct": chosen == found.answer,
        "explain_tr": found.explain_tr,
        "key_line": found.key_line,
        "script": json.loads(found.script_json or "[]"),
    }


@router.get("/audio/{reel_id}")
def audio(reel_id: str, db: Session = Depends(get_db)):
    found = db.get(AkisReel, reel_id)
    path = Path(found.audio_path) if found and found.audio_path else None
    if not found or not found.published or not path or not path.exists():
        raise HTTPException(404, "Ses bulunamadı")
    return FileResponse(path, media_type="audio/mpeg", filename=f"{reel_id}.mp3")


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=4000)


class ChatIn(BaseModel):
    reel_id: str = Field(min_length=1, max_length=64)
    choice: str = Field(default="", max_length=1)
    messages: list[Message] = Field(min_length=1, max_length=24)


def _chat_system() -> str:
    return (settings.content_dir / "prompts" / "akis_chat_system.txt").read_text(encoding="utf-8")


def _context(found: AkisReel, choice: str) -> str:
    options = json.loads(found.options_json or "{}")
    if found.kind == "sorular":
        lines = "\n".join(
            f"{line.get('speaker', '?')}: {line.get('text', '')}"
            for line in json.loads(found.script_json or "[]")
        )
        source = f"Transcript:\n{lines}\nSupporting line: {found.key_line or '(none)'}"
    elif found.kind == "kelime":
        source = f"Text:\n{found.body}\nCorrect spelling: {found.key_line or '(none)'}"
    else:
        source = f"Text (___ marks the gap):\n{found.body}"
    return (
        "CURRENT CARD\n"
        f"Type: {found.kind}\nLevel: {found.level}\nTitle: {found.title}\n{source}\n\n"
        f"Question: {found.stem}\nOptions: {json.dumps(options, ensure_ascii=False)}\n"
        f"Correct key: {found.answer}\nStored explanation: {found.explain_tr}\n"
        f"Student picked: {choice.upper() or '(not answered)'}\n"
    )


@router.get("/chat/status")
def chat_status():
    summary = active_summary()
    return {"ready": bool(llm_available() and summary["ready"]), "active": summary}


@router.post("/chat")
def chat(
    body: ChatIn,
    db: Session = Depends(get_db),
    _human=Depends(require_human),
    _rate=Depends(rate_limit_akis_chat),
    _slot=Depends(limit_ai_concurrency),
):
    if not llm_available() or not active_summary()["ready"]:
        raise HTTPException(503, "Sohbet şu an kapalı. Site sahibi panelden bir model seçmeli.")
    found = db.get(AkisReel, body.reel_id)
    if not found or not found.published:
        raise HTTPException(404, "Kart bulunamadı")
    history = [message for message in body.messages if message.role in {"user", "assistant"}]
    if not history or history[-1].role != "user":
        raise HTTPException(400, "Son mesaj kullanıcı mesajı olmalı.")
    payload = [message.model_dump() for message in history]
    payload[-1]["content"] = f"{_context(found, body.choice)}\nSTUDENT: {payload[-1]['content']}"
    try:
        reply = llm_chat(_chat_system(), payload).strip()
    except LLMError as exc:
        raise HTTPException(502, str(exc)) from exc
    return {"reply": reply}
