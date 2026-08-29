from __future__ import annotations

import json

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..config import settings
from ..db import get_db
from ..models import Attempt
from ..rate_limit import rate_limit_explain
from ..services.llm import LLMError, active_summary, complete, llm_available

router = APIRouter(prefix="/api", tags=["explain"])


class ExplainIn(BaseModel):
    attempt_id: str
    question_id: str
    message: str


def _explain_system() -> str:
    return (settings.content_dir / "prompts" / "explain_system.txt").read_text(encoding="utf-8")


@router.post("/explain")
def explain(body: ExplainIn, db: Session = Depends(get_db), _=Depends(rate_limit_explain)):
    if not llm_available():
        raise HTTPException(503, "Açıklama sohbeti şu an kapalı. Testler yine de çözülebilir.")
    if not active_summary()["ready"]:
        raise HTTPException(503, "Model seçilmedi. Site sahibi panelden bir model seçmeli.")
    if len(body.message.strip()) < 2:
        raise HTTPException(400, "Bir soru yaz.")
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
    user = (
        f"Source content: {json.dumps(source_content, ensure_ascii=False)}\n"
        f"Question: {question.stem}\n"
        f"Options: {json.dumps(options, ensure_ascii=False)}\n"
        f"Correct key: {question.answer}\n"
        f"Student chose: {chosen or '(blank)'}\n"
        f"Stored rationale: {question.rationale}\n"
        f"Student message: {body.message.strip()}\n"
    )
    try:
        text = complete(_explain_system(), user, json_mode=False)
    except LLMError as exc:
        raise HTTPException(502, str(exc)) from exc
    return {"reply": text.strip()}
