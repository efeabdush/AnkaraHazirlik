import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.config import Settings, settings
from app.main import app
from app.routers import admin


def test_railway_environment_enables_production_guards():
    production = Settings(app_env="development", railway_environment="production")

    assert production.is_production is True
    assert production.admin_key_management_enabled is False


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
