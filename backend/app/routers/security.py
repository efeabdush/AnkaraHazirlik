from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import json
import time
import uuid
from urllib.parse import urlparse

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field

from ..config import settings
from ..rate_limit import _client_ip, _client_key, rate_limit_turnstile

router = APIRouter(prefix="/api/security", tags=["security"])
human_header = APIKeyHeader(name="X-Human-Token", auto_error=False)


class TurnstileIn(BaseModel):
    token: str = Field(min_length=1, max_length=2048)


def _encode_part(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode().rstrip("=")


def _decode_part(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def _session_secret() -> bytes:
    value = settings.turnstile_session_secret or settings.admin_secret or settings.turnstile_secret_key
    return value.encode()


def _create_human_session(request: Request) -> tuple[str, int]:
    expires_at = int(time.time()) + max(5, settings.turnstile_session_minutes) * 60
    payload = _encode_part(
        json.dumps(
            {"exp": expires_at, "ip": _client_key(request), "v": 1},
            separators=(",", ":"),
        ).encode()
    )
    signature = _encode_part(hmac.new(_session_secret(), payload.encode(), hashlib.sha256).digest())
    return f"{payload}.{signature}", expires_at


def _valid_human_session(token: str, request: Request) -> bool:
    if len(token) > 1024:
        return False
    try:
        payload, supplied_signature = token.split(".", 1)
        expected_signature = _encode_part(hmac.new(_session_secret(), payload.encode(), hashlib.sha256).digest())
        if not hmac.compare_digest(supplied_signature, expected_signature):
            return False
        data = json.loads(_decode_part(payload))
        return (
            int(data.get("exp", 0)) >= int(time.time())
            and data.get("ip") == _client_key(request)
            and data.get("v") == 1
        )
    except (ValueError, TypeError, json.JSONDecodeError, binascii.Error, UnicodeDecodeError):
        return False


def _allowed_hostnames() -> set[str]:
    explicit = {item.strip().lower() for item in settings.turnstile_allowed_hostnames.split(",") if item.strip()}
    if explicit:
        return explicit
    return {
        parsed.hostname.lower()
        for item in settings.cors_origins.split(",")
        if (parsed := urlparse(item.strip())).hostname
    }


async def _verify_turnstile(token: str, request: Request) -> None:
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                "https://challenges.cloudflare.com/turnstile/v0/siteverify",
                data={
                    "secret": settings.turnstile_secret_key,
                    "response": token,
                    "remoteip": _client_ip(request),
                    "idempotency_key": str(uuid.uuid4()),
                },
            )
            response.raise_for_status()
            result = response.json()
    except (httpx.HTTPError, ValueError) as exc:
        raise HTTPException(502, "İnsan doğrulama servisine şu an ulaşılamıyor. Biraz sonra tekrar dene.") from exc
    if not isinstance(result, dict):
        raise HTTPException(502, "İnsan doğrulama servisi geçersiz bir yanıt verdi.")
    hostname = str(result.get("hostname", "")).lower()
    allowed = _allowed_hostnames()
    if not result.get("success") or (allowed and hostname not in allowed):
        raise HTTPException(403, "İnsan doğrulaması başarısız oldu. Kutuyu yenileyip tekrar dene.")
    action = str(result.get("action", ""))
    if action and action != "practice":
        raise HTTPException(403, "İnsan doğrulaması bu işlem için geçerli değil.")


def require_human(request: Request, token: str | None = Depends(human_header)) -> None:
    if not settings.turnstile_enabled:
        return
    if not token or not _valid_human_session(token, request):
        raise HTTPException(
            403,
            "Devam etmek için sayfadaki insan doğrulamasını tamamla.",
            headers={"X-Human-Verification": "required"},
        )


@router.get("/config")
def security_config():
    return {
        "turnstile_enabled": settings.turnstile_enabled,
        "turnstile_site_key": settings.turnstile_site_key if settings.turnstile_enabled else "",
        "session_minutes": settings.turnstile_session_minutes,
    }


@router.post("/verify")
async def verify_human(body: TurnstileIn, request: Request, _rate=Depends(rate_limit_turnstile)):
    if not settings.turnstile_enabled:
        raise HTTPException(404, "İnsan doğrulaması etkin değil.")
    await _verify_turnstile(body.token, request)
    session_token, expires_at = _create_human_session(request)
    return {"human_token": session_token, "expires_at": expires_at}
