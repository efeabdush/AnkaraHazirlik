import threading

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from .config import settings
from .db import Base, SessionLocal, engine, ensure_schema
from .models import Setting
from .providers import KEY_ENVS, set_panel_key
from .routers import admin, akis, evaluate, explain, public, security, transcribe
from .services.akis_seed import seed_akis
from .services.llm import set_active
from .services.seed import seed_if_empty

Base.metadata.create_all(bind=engine)
ensure_schema()

app = FastAPI(
    title="Hazırlık Prep API",
    version="0.1.0",
    docs_url=None if settings.is_production else "/docs",
    redoc_url=None if settings.is_production else "/redoc",
    openapi_url=None if settings.is_production else "/openapi.json",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["Accept", "Content-Type", "X-Admin-Secret", "X-Human-Token"],
    expose_headers=["Retry-After", "X-Human-Verification"],
)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Permissions-Policy"] = "camera=(), geolocation=(), microphone=()"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    if settings.is_production:
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
    if request.url.path.startswith("/api/admin"):
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Robots-Tag"] = "noindex, nofollow"
    return response
app.include_router(public.router)
app.include_router(akis.router)
app.include_router(security.router)
app.include_router(explain.router)
app.include_router(evaluate.router)
app.include_router(transcribe.router)
app.include_router(admin.router)


def _seed_worker() -> None:
    db = SessionLocal()
    try:
        seed_if_empty(db)
        seed_akis(db)
    finally:
        db.close()


def _restore_saved_config() -> None:
    db = SessionLocal()
    try:
        for key_env in KEY_ENVS:
            row = db.get(Setting, f"key:{key_env}")
            if row and row.value:
                set_panel_key(key_env, row.value)
        provider = db.get(Setting, "llm_provider")
        model = db.get(Setting, "llm_model")
        choice = _startup_model_choice(
            provider.value if provider else "",
            model.value if model else "",
        )
        if choice:
            set_active(*choice)
    finally:
        db.close()


def _startup_model_choice(saved_provider: str, saved_model: str) -> tuple[str, str] | None:
    """Use explicit production variables instead of a stale admin-panel choice."""
    env_provider = settings.llm_provider.strip()
    env_model = settings.llm_model.strip()
    if settings.is_production and env_provider and env_model:
        return env_provider, env_model
    if saved_provider.strip() and saved_model.strip():
        return saved_provider.strip(), saved_model.strip()
    if env_provider and env_model:
        return env_provider, env_model
    return None


@app.on_event("startup")
def startup() -> None:
    _restore_saved_config()
    threading.Thread(target=_seed_worker, daemon=True).start()


@app.get("/")
def root():
    return RedirectResponse(settings.public_site_url)


@app.get("/api/health")
def health():
    return {"ok": True}
