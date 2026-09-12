import uuid

import pytest
from fastapi import HTTPException, Request
from fastapi.testclient import TestClient
from sqlalchemy import delete

from app.config import Settings, settings
from app.auth import require_admin
from app.db import SessionLocal
from app.main import _startup_model_choice, app
from app.models import ApiUsage
from app.rate_limit import _client_ip, _persistent_rate_limit
from app.routers import admin
from app.routers.security import _create_human_session, _valid_human_session, require_human


def _request(headers: list[tuple[bytes, bytes]] | None = None) -> Request:
    return Request({"type": "http", "method": "GET", "path": "/", "headers": headers or [], "client": ("127.0.0.1", 1)})


def test_passwordless_admin_is_opt_in_when_no_env_file_exists():
    defaults = Settings(_env_file=None)

    assert defaults.local_admin_passwordless is False


def test_railway_environment_enables_production_guards():
    production = Settings(app_env="development", railway_environment="production")

    assert production.is_production is True
    assert production.admin_key_management_enabled is False
    assert production.local_admin_passwordless_enabled is False


def test_local_admin_is_passwordless_only_for_loopback(monkeypatch):
    monkeypatch.setattr(settings, "app_env", "development")
    monkeypatch.setattr(settings, "railway_environment", "")
    monkeypatch.setattr(settings, "local_admin_passwordless", True)
    monkeypatch.setattr(settings, "admin_secret", "")

    require_admin(_request())

    remote = Request({"type": "http", "method": "GET", "path": "/", "headers": [], "client": ("203.0.113.8", 1)})
    with pytest.raises(HTTPException) as exc:
        require_admin(remote)
    assert exc.value.status_code == 401


def test_production_admin_still_requires_secret(monkeypatch):
    monkeypatch.setattr(settings, "app_env", "production")
    monkeypatch.setattr(settings, "railway_environment", "")
    monkeypatch.setattr(settings, "local_admin_passwordless", True)
    monkeypatch.setattr(settings, "admin_secret", "production-secret")

    with pytest.raises(HTTPException) as exc:
        require_admin(_request())
    assert exc.value.status_code == 401

    require_admin(_request(), "production-secret")


def test_production_environment_model_overrides_saved_admin_choice(monkeypatch):
    monkeypatch.setattr(settings, "railway_environment", "production")
    monkeypatch.setattr(settings, "llm_provider", "openrouter")
    monkeypatch.setattr(settings, "llm_model", "deepseek/deepseek-v4-pro-0813")

    assert _startup_model_choice("opencode-go", "glm-5.2") == (
        "openrouter",
        "deepseek/deepseek-v4-pro-0813",
    )


def test_admin_key_management_is_blocked_in_production(monkeypatch):
    monkeypatch.setattr(settings, "railway_environment", "production")

    with pytest.raises(HTTPException) as exc:
        admin._require_key_management()

    assert exc.value.status_code == 403


def test_api_security_headers_are_present():
    response = TestClient(app).get("/api/health")

    assert response.status_code == 200
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "no-referrer"


def test_railway_real_ip_is_used_instead_of_spoofable_forwarded_prefix():
    request = _request([(b"x-real-ip", b"203.0.113.9"), (b"x-forwarded-for", b"198.51.100.2, 10.0.0.1")])

    assert _client_ip(request) == "203.0.113.9"


def test_production_usage_counter_is_persistent_and_enforced():
    bucket = f"test-{uuid.uuid4()}"
    request = _request()
    try:
        _persistent_rate_limit(request, bucket, bucket, hourly_limit=1, daily_limit=10)
        with pytest.raises(HTTPException) as exc:
            _persistent_rate_limit(request, bucket, bucket, hourly_limit=1, daily_limit=10)
        assert exc.value.status_code == 429
        assert exc.value.headers and "Retry-After" in exc.value.headers
    finally:
        with SessionLocal() as db:
            db.execute(delete(ApiUsage).where(ApiUsage.key.contains(bucket)))
            db.commit()


def test_human_session_is_signed_ip_bound_and_tamper_resistant(monkeypatch):
    monkeypatch.setattr(settings, "turnstile_site_key", "site-key")
    monkeypatch.setattr(settings, "turnstile_secret_key", "secret-key")
    monkeypatch.setattr(settings, "turnstile_session_secret", "session-key")
    request = _request([(b"x-real-ip", b"203.0.113.9")])

    token, _ = _create_human_session(request)

    assert _valid_human_session(token, request) is True
    assert _valid_human_session(f"{token}x", request) is False
    require_human(request, token)
    with pytest.raises(HTTPException) as exc:
        require_human(_request([(b"x-real-ip", b"203.0.113.10")]), token)
    assert exc.value.status_code == 403
