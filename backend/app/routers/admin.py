from __future__ import annotations

import json
import threading

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..auth import require_admin
from ..config import settings
from ..db import SessionLocal, get_db
from ..models import GenerationJob, Setting, Test
from ..providers import (
    DEFAULT_ORDER,
    KEY_ENVS,
    PROVIDERS,
    get_provider,
    mask_key,
    panel_key,
    set_panel_key,
)
from ..services.generate import run_generation_job
from ..services.validator import ACADEMIC_KINDS
from ..services.glossary import local_glossary, merge_glossary, pack_from_test, run_glossary_job
from ..services.llm import (
    LLMError,
    active_summary,
    list_models,
    llm_available,
    set_active,
)

router = APIRouter(prefix="/api/admin", tags=["admin"], dependencies=[Depends(require_admin)])


def _glossary_parts(t: Test) -> tuple[list, dict]:
    try:
        data = json.loads(t.glossary_json or "[]")
    except json.JSONDecodeError:
        return [], {}
    if isinstance(data, dict):
        entries = data.get("entries") or []
        words = data.get("words") or {}
        return (
            entries if isinstance(entries, list) else [],
            words if isinstance(words, dict) else {},
        )
    return (data if isinstance(data, list) else []), {}


def _glossary_n(t: Test) -> int:
    entries, words = _glossary_parts(t)
    return len(entries) + len(words)


class GenerateIn(BaseModel):
    kind: str
    topic: str = ""
    publish: bool = True


class PublishIn(BaseModel):
    published: bool


class ModelIn(BaseModel):
    provider: str
    model: str


class KeyIn(BaseModel):
    key_env: str
    api_key: str


def _save_setting(db: Session, key: str, value: str) -> None:
    row = db.get(Setting, key)
    if row:
        row.value = value
    else:
        db.add(Setting(key=key, value=value))


def _require_key_management() -> None:
    if not settings.admin_key_management_enabled:
        raise HTTPException(403, "Production ortamında API anahtarları yalnızca Railway variables üzerinden yönetilir.")


@router.get("/status")
def admin_status():
    return {"ok": True, "llm": llm_available(), "active": active_summary()}


@router.get("/providers")
def providers():
    return {
        "active": active_summary(),
        "key_management_enabled": settings.admin_key_management_enabled,
        "providers": [
            {
                "id": PROVIDERS[pid].id,
                "label": PROVIDERS[pid].label,
                "note": PROVIDERS[pid].note,
                "key_env": PROVIDERS[pid].key_env,
                "configured": PROVIDERS[pid].configured,
                "key_source": PROVIDERS[pid].key_source,
                "key_masked": mask_key(PROVIDERS[pid].api_key),
            }
            for pid in DEFAULT_ORDER
        ],
    }


@router.post("/keys")
def save_key(body: KeyIn, db: Session = Depends(get_db)):
    """Store an API key from the panel, but only if it actually works."""

    _require_key_management()

    key_env = body.key_env.strip().upper()
    if key_env not in KEY_ENVS:
        raise HTTPException(400, "Bilinmeyen anahtar alanı")
    api_key = body.api_key.strip()
    if not api_key:
        raise HTTPException(400, "Anahtar boş")

    previous = panel_key(key_env)
    set_panel_key(key_env, api_key)

    probe = next((PROVIDERS[pid] for pid in DEFAULT_ORDER if PROVIDERS[pid].key_env == key_env), None)
    if probe is None:
        set_panel_key(key_env, previous)
        raise HTTPException(400, "Bu anahtarı kullanan sağlayıcı yok")

    try:
        models = list_models(probe)
    except Exception as exc:  # noqa: BLE001
        set_panel_key(key_env, previous)
        raise HTTPException(400, f"Anahtar çalışmadı: {exc}") from exc

    _save_setting(db, f"key:{key_env}", api_key)
    db.commit()
    return {
        "key_env": key_env,
        "key_masked": mask_key(api_key),
        "model_count": len(models),
        "tested_with": probe.label,
    }


@router.delete("/keys/{key_env}")
def delete_key(key_env: str, db: Session = Depends(get_db)):
    _require_key_management()
    key_env = key_env.strip().upper()
    if key_env not in KEY_ENVS:
        raise HTTPException(400, "Bilinmeyen anahtar alanı")
    set_panel_key(key_env, "")
    row = db.get(Setting, f"key:{key_env}")
    if row:
        db.delete(row)
        db.commit()
    return {"key_env": key_env, "removed": True}


@router.get("/models")
def models(provider: str):
    p = get_provider(provider)
    if not p:
        raise HTTPException(404, "Sağlayıcı yok")
    if not p.configured:
        raise HTTPException(400, f"{p.label} için {p.key_env} tanımlı değil.")
    try:
        return {"provider": p.id, "models": list_models(p)}
    except LLMError as exc:
        raise HTTPException(502, str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(502, f"{p.label} model listesi alınamadı: {exc}") from exc


@router.post("/model")
def choose_model(body: ModelIn, db: Session = Depends(get_db)):
    p = get_provider(body.provider)
    if not p:
        raise HTTPException(404, "Sağlayıcı yok")
    if not p.configured:
        raise HTTPException(400, f"{p.label} için {p.key_env} tanımlı değil.")
    if not body.model.strip():
        raise HTTPException(400, "Model seç")
    _save_setting(db, "llm_provider", p.id)
    _save_setting(db, "llm_model", body.model.strip())
    db.commit()
    set_active(p.id, body.model.strip())
    return active_summary()


@router.get("/tests")
def admin_tests(db: Session = Depends(get_db)):
    tests = db.query(Test).order_by(Test.created_at.desc()).all()
    return [
        {
            "id": t.id,
            "kind": t.kind,
            "title": t.title,
            "topic": t.topic,
            "published": t.published,
            "source": t.source,
            "duration_sec": t.duration_sec,
            "glossary_n": _glossary_n(t),
            "glossary_entries": len(_glossary_parts(t)[0]),
            "glossary_words": len(_glossary_parts(t)[1]),
        }
        for t in tests
    ]


@router.post("/tests/{test_id}/publish")
def publish_test(test_id: str, body: PublishIn, db: Session = Depends(get_db)):
    t = db.get(Test, test_id)
    if not t:
        raise HTTPException(404, "Test yok")
    t.published = body.published
    db.commit()
    return {"id": t.id, "published": t.published}


@router.post("/tests/{test_id}/glossary")
def rebuild_glossary(test_id: str, db: Session = Depends(get_db)):
    t = db.get(Test, test_id)
    if not t:
        raise HTTPException(404, "Test yok")
    pack = pack_from_test(t)
    existing_entries, existing_words = _glossary_parts(t)
    local = local_glossary(pack)
    merged = merge_glossary({"entries": existing_entries, "words": existing_words}, local)
    t.glossary_json = json.dumps(
        {"entries": merged["entries"], "words": merged["words"]},
        ensure_ascii=False,
    )
    db.commit()

    summary = active_summary()
    if not llm_available() or not summary["ready"]:
        return {
            "id": t.id,
            "job_id": None,
            "status": "local",
            "glossary_n": _glossary_n(t),
            "glossary_entries": len(merged["entries"]),
            "glossary_words": len(merged["words"]),
            "note": "Kelime paketi kaydedildi. Cümle çevirisi için panelden bir model seç, sonra tekrar bas.",
        }

    job = GenerationJob(kind="glossary", topic=t.title, test_id=t.id, status="queued")
    db.add(job)
    db.commit()
    db.refresh(job)
    job_id = job.id

    def worker() -> None:
        session = SessionLocal()
        try:
            run_glossary_job(session, job_id)
        finally:
            session.close()

    threading.Thread(target=worker, daemon=True).start()
    return {
        "id": t.id,
        "job_id": job.id,
        "status": "queued",
        "glossary_n": _glossary_n(t),
        "glossary_entries": len(merged["entries"]),
        "glossary_words": len(merged["words"]),
        "note": "Kelime paketi kaydedildi. Cümle çevirisi arka planda üretiliyor.",
    }


@router.post("/generate")
def generate(body: GenerateIn, db: Session = Depends(get_db)):
    if body.kind not in {"conversation", "lecture", *ACADEMIC_KINDS}:
        raise HTTPException(400, "Bilinmeyen içerik türü")
    summary = active_summary()
    if not llm_available():
        raise HTTPException(503, "Sunucuda sağlayıcı anahtarı yok. .env dosyasına anahtar ekle.")
    if not summary["ready"]:
        raise HTTPException(400, "Önce bir model seç.")
    job = GenerationJob(kind=body.kind, topic=body.topic.strip(), status="queued")
    db.add(job)
    db.commit()
    db.refresh(job)

    job_id = job.id

    def worker() -> None:
        session = SessionLocal()
        try:
            run_generation_job(session, job_id)
            if not body.publish:
                job2 = session.get(GenerationJob, job_id)
                if job2 and job2.test_id:
                    t = session.get(Test, job2.test_id)
                    if t:
                        t.published = False
                        session.commit()
        finally:
            session.close()

    threading.Thread(target=worker, daemon=True).start()
    return {"job_id": job.id}


@router.get("/jobs/{job_id}")
def job_status(job_id: str, db: Session = Depends(get_db)):
    job = db.get(GenerationJob, job_id)
    if not job:
        raise HTTPException(404, "İş yok")
    return {
        "id": job.id,
        "status": job.status,
        "kind": job.kind,
        "topic": job.topic,
        "test_id": job.test_id or None,
        "error": job.error or None,
    }
