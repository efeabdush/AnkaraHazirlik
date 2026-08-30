from __future__ import annotations

import json
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..config import settings
from ..db import get_db
from ..models import Attempt
from ..rate_limit import limit_ai_concurrency, rate_limit_explain
from ..services.llm import LLMError, active_summary, complete, llm_available
from .security import require_human

router = APIRouter(prefix="/api", tags=["explain"])


class ExplainMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=3000)


class ExplainIn(BaseModel):
    attempt_id: str
    question_id: str
    message: str = Field(min_length=2, max_length=3000)
    messages: list[ExplainMessage] = Field(default_factory=list, max_length=12)


def _explain_system() -> str:
    return (settings.content_dir / "prompts" / "explain_system.txt").read_text(encoding="utf-8")


@router.post("/explain")
def explain(
    body: ExplainIn,
    db: Session = Depends(get_db),
    _human=Depends(require_human),
    _rate=Depends(rate_limit_explain),
    _slot=Depends(limit_ai_concurrency),
):
    if not llm_available():
        raise HTTPException(503, "Açıklama sohbeti şu an kapalı. Testler yine de çözülebilir.")
    if not active_summary()["ready"]:
        raise HTTPException(503, "Model seçilmedi. Site sahibi panelden bir model seçmeli.")
    attempt = db.get(Attempt, body.attempt_id)
    if not attempt:
        raise HTTPException(404, "Deneme bulunamadı")
    question = next((q for q in attempt.test.questions if q.id == body.question_id), None)
    if not question:
        raise HTTPException(404, "Soru bulunamadı")
    answers = json.loads(attempt.answers_json)
    chosen = (answers.get(question.id) or "").upper()
    options = json.loads(question.options_json)
    source_content = json.loads(attempt.test.content_json or "{}")
    history = [item for item in body.messages if item.role in {"user", "assistant"}]
    if not history or history[-1].role != "user" or history[-1].content.strip() != body.message.strip():
        history.append(ExplainMessage(role="user", content=body.message.strip()))
    history = history[-12:]
    conversation = "\n".join(f"{item.role.upper()}: {item.content.strip()}" for item in history)
    user = (
        f"Source content: {json.dumps(source_content, ensure_ascii=False)}\n"
        f"Question: {question.stem}\n"
        f"Options: {json.dumps(options, ensure_ascii=False)}\n"
        f"Correct key: {question.answer}\n"
        f"Student chose: {chosen or '(blank)'}\n"
        f"Stored rationale: {question.rationale}\n"
        "The conversation below belongs only to this question. Use earlier turns when the student asks a follow-up.\n"
        f"Conversation:\n{conversation}\n"
    )
    try:
        text = complete(_explain_system(), user, json_mode=False)
    except LLMError as exc:
        raise HTTPException(502, str(exc)) from exc
    return {"reply": text.strip()}
