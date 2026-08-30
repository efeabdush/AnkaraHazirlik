from fastapi.testclient import TestClient

from app.config import settings
from app.main import app
from app.routers import contact


class _Response:
    def raise_for_status(self) -> None:
        return None


class _AsyncClient:
    def __init__(self, captured: dict, **_kwargs):
        self.captured = captured

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_args):
        return None

    async def post(self, url: str, **kwargs):
        self.captured.update({"url": url, **kwargs})
        return _Response()


def test_contact_config_is_disabled_without_server_credentials(monkeypatch):
    monkeypatch.setattr(settings, "resend_api_key", "")
    monkeypatch.setattr(settings, "contact_to_email", "")

    response = TestClient(app).get("/api/contact/config")

    assert response.status_code == 200
    assert response.json() == {"enabled": False}


def test_contact_sends_email_without_persisting_message(monkeypatch):
    captured: dict = {}
    monkeypatch.setattr(settings, "resend_api_key", "resend-test")
    monkeypatch.setattr(settings, "contact_to_email", "owner@example.com")
    monkeypatch.setattr(settings, "contact_from_email", "Site <site@example.com>")
    monkeypatch.setattr(contact.httpx, "AsyncClient", lambda **kwargs: _AsyncClient(captured, **kwargs))

    response = TestClient(app).post(
        "/api/contact",
        json={
            "name": "Efe <script>",
            "category": "bug",
            "message": "Butonda <b>hata</b> görüyorum.",
            "website": "",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"ok": True}
    assert captured["url"] == "https://api.resend.com/emails"
    payload = captured["json"]
    assert payload["to"] == ["owner@example.com"]
    assert "reply_to" not in payload
    assert "<script>" not in payload["html"]
    assert "&lt;script&gt;" in payload["html"]
    assert "<b>hata</b>" not in payload["html"]


def test_contact_honeypot_does_not_call_delivery_service(monkeypatch):
    monkeypatch.setattr(settings, "resend_api_key", "")
    monkeypatch.setattr(settings, "contact_to_email", "")

    response = TestClient(app).post(
        "/api/contact",
        json={
            "name": "Spam Bot",
            "category": "general",
            "message": "This is definitely automated.",
            "website": "https://spam.invalid",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"ok": True}
