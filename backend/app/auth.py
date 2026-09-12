from ipaddress import ip_address

from fastapi import Header, HTTPException, Request

from .config import settings


def _is_loopback_client(request: Request) -> bool:
    if request.client is None:
        return False
    try:
        return ip_address(request.client.host).is_loopback
    except ValueError:
        return False


def require_admin(request: Request, x_admin_secret: str = Header(default="", alias="X-Admin-Secret")) -> None:
    # The clone-and-run experience is intentionally frictionless on localhost.
    # Production never receives this bypass, even if the flag was left enabled.
    if settings.local_admin_passwordless_enabled and _is_loopback_client(request):
        return
    if not settings.admin_secret or x_admin_secret != settings.admin_secret:
        raise HTTPException(status_code=401, detail="Admin yetkisi gerekli.")
