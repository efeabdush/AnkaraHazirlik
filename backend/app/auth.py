from fastapi import Header, HTTPException

from .config import settings


def require_admin(x_admin_secret: str = Header(default="", alias="X-Admin-Secret")) -> None:
    if not settings.admin_secret or x_admin_secret != settings.admin_secret:
        raise HTTPException(status_code=401, detail="Admin yetkisi gerekli.")
