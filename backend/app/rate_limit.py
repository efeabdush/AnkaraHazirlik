from __future__ import annotations

from collections import defaultdict, deque
from time import time

from fastapi import HTTPException, Request

from .config import settings


_hits: dict[str, deque[float]] = defaultdict(deque)


def _rate_limit(request: Request, bucket: str, limit: int) -> None:
    ip = request.client.host if request.client else "unknown"
    now = time()
    window = 3600
    q = _hits[f"{bucket}:{ip}"]
    while q and now - q[0] > window:
        q.popleft()
    if len(q) >= limit:
        raise HTTPException(status_code=429, detail="Şimdilik yeterince soru sordun. Biraz sonra tekrar dene.")
    q.append(now)


def rate_limit_explain(request: Request) -> None:
    _rate_limit(request, "explain", settings.explain_rate_limit_per_hour)


def rate_limit_evaluate(request: Request) -> None:
    _rate_limit(request, "evaluate", settings.evaluation_rate_limit_per_hour)


def rate_limit_coach(request: Request) -> None:
    _rate_limit(request, "coach", settings.coach_rate_limit_per_hour)


def rate_limit_transcribe(request: Request) -> None:
    _rate_limit(request, "transcribe", settings.transcribe_rate_limit_per_hour)
