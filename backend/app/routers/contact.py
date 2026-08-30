from __future__ import annotations

import html
import re
from typing import Literal

import httpx
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator

from ..config import settings
from ..rate_limit import rate_limit_contact
from .security import require_human

router = APIRouter(prefix="/api/contact", tags=["contact"])

EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
CATEGORY_LABELS = {
    "bug": "Hata bildirimi",
    "content": "İçerik önerisi",
    "general": "Genel mesaj",
}


class ContactIn(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: str = Field(min_length=5, max_length=160)
    category: Literal["bug", "content", "general"] = "general"
    message: str = Field(min_length=10, max_length=4000)
    website: str = Field(default="", max_length=200)

    @field_validator("name", "email", "message", mode="before")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return str(value).strip()

    @field_validator("email")
    @classmethod
    def valid_email(cls, value: str) -> str:
        if not EMAIL_PATTERN.fullmatch(value):
            raise ValueError("Geçerli bir e-posta adresi yaz.")
        return value


@router.get("/config")
def contact_config():
    return {"enabled": settings.contact_enabled}


@router.post("")
async def send_contact(
    body: ContactIn,
    _human=Depends(require_human),
    _rate=Depends(rate_limit_contact),
):
    # Görünmez alanı botlar doldurur. Dışarıya hata vermeden mesajı yok say.
    if body.website.strip():
        return {"ok": True}
    if not settings.contact_enabled:
        raise HTTPException(503, "İletişim kutusu henüz etkinleştirilmedi.")

    category = CATEGORY_LABELS[body.category]
    subject = f"[Ankara Hazırlık] {category} — {body.name}"
    plain = (
        f"Kategori: {category}\n"
        f"Gönderen: {body.name} <{body.email}>\n\n"
        f"{body.message}\n"
    )
    markup = (
        f"<p><strong>Kategori:</strong> {html.escape(category)}</p>"
        f"<p><strong>Gönderen:</strong> {html.escape(body.name)} "
        f"&lt;{html.escape(body.email)}&gt;</p>"
        f"<hr><p>{html.escape(body.message).replace(chr(10), '<br>')}</p>"
    )
    try:
        async with httpx.AsyncClient(timeout=12) as client:
            response = await client.post(
                "https://api.resend.com/emails",
                headers={
                    "Authorization": f"Bearer {settings.resend_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "from": settings.contact_from_email,
                    "to": [settings.contact_to_email],
                    "reply_to": body.email,
                    "subject": subject,
                    "text": plain,
                    "html": markup,
                },
            )
            response.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(502, "Mesaj şu an gönderilemedi. Biraz sonra tekrar dene.") from exc
    return {"ok": True}
