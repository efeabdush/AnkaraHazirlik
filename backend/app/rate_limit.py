from __future__ import annotations

import asyncio
import hashlib
import threading
from collections import defaultdict, deque
from collections.abc import Generator
from time import time

from fastapi import HTTPException, Request
from sqlalchemy import delete

from .config import settings
from .db import SessionLocal
from .models import ApiUsage


_hits: dict[str, deque[float]] = defaultdict(deque)
_usage_lock = threading.Lock()
_last_prune = 0.0
_ai_slots = threading.BoundedSemaphore(max(1, settings.ai_max_concurrent))
_transcribe_slots = asyncio.BoundedSemaphore(max(1, settings.transcribe_max_concurrent))


def _client_ip(request: Request) -> str:
    railway_ip = request.headers.get("X-Real-IP", "").strip()
    if railway_ip:
        return railway_ip
    forwarded = request.headers.get("X-Forwarded-For", "")
    if forwarded:
        # Fallback for non-Railway reverse proxies. Prefer the final hop so a
        # caller cannot select the identity with a forged leading entry.
        return forwarded.split(",")[-1].strip()
    return request.client.host if request.client else "unknown"


def _client_key(request: Request) -> str:
    secret = settings.rate_limit_hash_secret or settings.admin_secret or "hazirlik-rate-limit"
    return hashlib.sha256(f"{secret}:{_client_ip(request)}".encode()).hexdigest()[:32]


def _memory_rate_limit(client_key: str, bucket: str, limit: int) -> None:
    now = time()
    q = _hits[f"{bucket}:{client_key}"]
    while q and now - q[0] > 3600:
        q.popleft()
    if len(q) >= limit:
        retry_after = max(1, round(3600 - (now - q[0])))
        raise HTTPException(
            status_code=429,
            detail="Bu işlem için saatlik kullanım sınırına ulaştın. Biraz sonra tekrar dene.",
            headers={"Retry-After": str(retry_after)},
        )
    q.append(now)


def _increment_persistent(key: str, expires_at: int) -> int:
    global _last_prune
    now = int(time())
    with _usage_lock:
        with SessionLocal() as db:
            row = db.get(ApiUsage, key)
            if row is None:
                row = ApiUsage(key=key, count=1, expires_at=expires_at)
                db.add(row)
            else:
                row.count += 1
                row.expires_at = expires_at
            count = row.count
            if now - _last_prune >= 3600:
                db.execute(delete(ApiUsage).where(ApiUsage.expires_at < now))
                _last_prune = float(now)
            db.commit()
            return count


def _persistent_rate_limit(
    request: Request,
    hourly_bucket: str,
    daily_bucket: str,
    hourly_limit: int,
    daily_limit: int,
) -> None:
    now = int(time())
    client_key = _client_key(request)
    hour_start = now - (now % 3600)
    day_start = now - (now % 86400)
    hourly_count = _increment_persistent(
        f"hour:{hourly_bucket}:{hour_start}:{client_key}",
        hour_start + 7200,
    )
    if hourly_count > hourly_limit:
        raise HTTPException(
            status_code=429,
            detail="Bu işlem için saatlik kullanım sınırına ulaştın. Biraz sonra tekrar dene.",
            headers={"Retry-After": str(max(1, hour_start + 3600 - now))},
        )
    daily_count = _increment_persistent(
        f"day:{daily_bucket}:{day_start}:global",
        day_start + 172800,
    )
    if daily_count > daily_limit:
        raise HTTPException(
            status_code=429,
            detail="Sitenin bugünkü güvenli kullanım kotası doldu. Yarın tekrar deneyebilirsin.",
            headers={"Retry-After": str(max(1, day_start + 86400 - now))},
        )


def _rate_limit(
    request: Request,
    hourly_bucket: str,
    daily_bucket: str,
    hourly_limit: int,
    daily_limit: int,
) -> None:
    # Production counters survive Railway restarts through the mounted database.
    # Local development remains disposable and does not pollute its database.
    if settings.is_production:
        _persistent_rate_limit(request, hourly_bucket, daily_bucket, hourly_limit, daily_limit)
    else:
        _memory_rate_limit(_client_key(request), hourly_bucket, hourly_limit)


def rate_limit_explain(request: Request) -> None:
    _rate_limit(request, "explain", "ai", settings.explain_rate_limit_per_hour, settings.ai_daily_request_limit)


def rate_limit_evaluate(request: Request) -> None:
    _rate_limit(request, "evaluate", "ai", settings.evaluation_rate_limit_per_hour, settings.ai_daily_request_limit)


def rate_limit_coach(request: Request) -> None:
    _rate_limit(request, "coach", "ai", settings.coach_rate_limit_per_hour, settings.ai_daily_request_limit)


def rate_limit_akis_chat(request: Request) -> None:
    _rate_limit(request, "akis-chat", "ai", settings.akis_chat_rate_limit_per_hour, settings.ai_daily_request_limit)


def rate_limit_transcribe(request: Request) -> None:
    _rate_limit(
        request,
        "transcribe",
        "transcribe",
        settings.transcribe_rate_limit_per_hour,
        settings.transcribe_daily_request_limit,
    )


def rate_limit_turnstile(request: Request) -> None:
    _rate_limit(
        request,
        "turnstile",
        "turnstile",
        settings.turnstile_rate_limit_per_hour,
        settings.turnstile_daily_request_limit,
    )


def limit_ai_concurrency() -> Generator[None, None, None]:
    if not _ai_slots.acquire(blocking=False):
        raise HTTPException(
            status_code=503,
            detail="Değerlendirme sistemi şu an dolu. Birkaç saniye sonra tekrar dene.",
            headers={"Retry-After": "10"},
        )
    try:
        yield
    finally:
        _ai_slots.release()


async def limit_transcribe_concurrency():
    try:
        await asyncio.wait_for(_transcribe_slots.acquire(), timeout=0.01)
    except TimeoutError as exc:
        raise HTTPException(
            status_code=503,
            detail="Ses çözümleme sistemi şu an dolu. Biraz sonra tekrar dene.",
            headers={"Retry-After": "15"},
        ) from exc
    try:
        yield
    finally:
        _transcribe_slots.release()
