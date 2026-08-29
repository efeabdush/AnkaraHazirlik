from __future__ import annotations

import json
import re

import httpx

from ..config import settings
from ..providers import Provider, first_configured, get_provider, rank_models


class LLMError(RuntimeError):
    pass


# ---------------------------------------------------------------- selection

_active: dict[str, str] = {"provider": "", "model": ""}


def set_active(provider_id: str, model: str) -> None:
    _active["provider"] = provider_id
    _active["model"] = model


def active_provider() -> Provider | None:
    if _active["provider"]:
        p = get_provider(_active["provider"])
        if p and p.configured:
            return p
    p = get_provider(settings.llm_provider)
    if p and p.configured:
        return p
    return first_configured()


def active_model() -> str:
    if _active["model"]:
        return _active["model"]
    if settings.llm_model:
        return settings.llm_model
    return ""


def llm_available() -> bool:
    return active_provider() is not None


def active_summary() -> dict:
    p = active_provider()
    return {
        "provider": p.id if p else None,
        "provider_label": p.label if p else None,
        "model": active_model() or None,
        "ready": bool(p and active_model()),
    }


# ---------------------------------------------------------------- models list


def list_models(provider: Provider) -> list[str]:
    if not provider.configured:
        raise LLMError(f"{provider.label} için anahtar yok.")

    if provider.id == "gemini":
        url = f"{provider.base_url}/models?key={provider.api_key}"
        with httpx.Client(timeout=30) as client:
            r = client.get(url)
            r.raise_for_status()
            data = r.json()
        ids = [
            m["name"].split("/")[-1]
            for m in data.get("models", [])
            if "generateContent" in (m.get("supportedGenerationMethods") or [])
        ]
        return rank_models(provider, ids)

    url = f"{provider.base_url}{provider.models_path}"
    with httpx.Client(timeout=30) as client:
        r = client.get(url, headers=_auth_headers(provider))
        r.raise_for_status()
        data = r.json()
    raw = data.get("data") if isinstance(data, dict) else data
    ids: list[str] = []
    for item in raw or []:
        if isinstance(item, str):
            ids.append(item)
        elif isinstance(item, dict):
            model_id = item.get("id") or item.get("name")
            if model_id:
                ids.append(str(model_id))
    if not ids:
        raise LLMError(f"{provider.label} model listesi boş döndü.")
    return rank_models(provider, ids)


# ---------------------------------------------------------------- completion


def _auth_headers(provider: Provider) -> dict[str, str]:
    headers = {"Authorization": f"Bearer {provider.api_key}"}
    if provider.id == "openrouter":
        headers["HTTP-Referer"] = settings.public_site_url
        headers["X-OpenRouter-Title"] = settings.public_site_name
    return headers


def complete(system: str, user: str, json_mode: bool = False) -> str:
    provider = active_provider()
    if not provider:
        raise LLMError("Sunucuda hiçbir sağlayıcı anahtarı tanımlı değil.")
    model = active_model()
    if not model:
        raise LLMError(f"{provider.label} için model seçilmedi. Panelden bir model seç.")

    if provider.id == "gemini":
        text = _gemini(provider, model, system, user, json_mode)
    elif provider.id == "opencode-zen" and model.lower().startswith("claude"):
        text = _anthropic_messages(provider, model, system, user)
    elif provider.id == "opencode-zen" and model.lower().startswith("gpt-"):
        text = _openai_responses(provider, model, system, user, json_mode)
    else:
        text = _openai_chat(provider, model, system, user, json_mode)

    return _extract_json(text) if json_mode else text


def _openai_chat(provider: Provider, model: str, system: str, user: str, json_mode: bool) -> str:
    body: dict = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.6,
    }
    if json_mode:
        body["response_format"] = {"type": "json_object"}
    with httpx.Client(timeout=180) as client:
        r = client.post(f"{provider.base_url}/chat/completions", headers=_auth_headers(provider), json=body)
        _raise_for_status(provider, r)
        data = r.json()
    try:
        return data["choices"][0]["message"]["content"] or ""
    except (KeyError, IndexError) as exc:
        raise LLMError(f"{provider.label} yanıtı okunamadı: {data}") from exc


def _openai_responses(provider: Provider, model: str, system: str, user: str, json_mode: bool) -> str:
    body: dict = {
        "model": model,
        "instructions": system,
        "input": user,
    }
    if json_mode:
        body["text"] = {"format": {"type": "json_object"}}
    with httpx.Client(timeout=180) as client:
        r = client.post(f"{provider.base_url}/responses", headers=_auth_headers(provider), json=body)
        _raise_for_status(provider, r)
        data = r.json()
    if isinstance(data.get("output_text"), str):
        return data["output_text"]
    chunks: list[str] = []
    for item in data.get("output") or []:
        for part in item.get("content") or []:
            if part.get("type") in {"output_text", "text"} and part.get("text"):
                chunks.append(part["text"])
    if not chunks:
        raise LLMError(f"{provider.label} yanıtı okunamadı: {data}")
    return "".join(chunks)


def _anthropic_messages(provider: Provider, model: str, system: str, user: str) -> str:
    headers = _auth_headers(provider)
    headers["anthropic-version"] = "2023-06-01"
    body = {
        "model": model,
        "system": system,
        "max_tokens": 8192,
        "messages": [{"role": "user", "content": user}],
    }
    with httpx.Client(timeout=180) as client:
        r = client.post(f"{provider.base_url}/messages", headers=headers, json=body)
        _raise_for_status(provider, r)
        data = r.json()
    chunks = [b.get("text", "") for b in data.get("content") or [] if b.get("type") == "text"]
    if not chunks:
        raise LLMError(f"{provider.label} yanıtı okunamadı: {data}")
    return "".join(chunks)


def _gemini(provider: Provider, model: str, system: str, user: str, json_mode: bool) -> str:
    url = f"{provider.base_url}/models/{model}:generateContent?key={provider.api_key}"
    generation_config: dict = {"temperature": 0.6, "maxOutputTokens": 8192}
    if json_mode:
        generation_config["responseMimeType"] = "application/json"
    payload = {
        "systemInstruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": [{"text": user}]}],
        "generationConfig": generation_config,
    }
    with httpx.Client(timeout=180) as client:
        r = client.post(url, json=payload)
        _raise_for_status(provider, r)
        data = r.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError) as exc:
        raise LLMError(f"Gemini yanıtı okunamadı: {data}") from exc


def _raise_for_status(provider: Provider, response: httpx.Response) -> None:
    if response.is_success:
        return
    detail = response.text[:500]
    raise LLMError(f"{provider.label} hatası {response.status_code}: {detail}")


# ---------------------------------------------------------------- helpers


def _extract_json(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return text


def parse_json_object(text: str) -> dict:
    blob = _extract_json(text)
    try:
        data = json.loads(blob)
    except json.JSONDecodeError:
        start = blob.find("{")
        end = blob.rfind("}")
        if start < 0 or end <= start:
            raise LLMError(f"JSON okunamadı: {blob[:240]}") from None
        try:
            data = json.loads(blob[start : end + 1])
        except json.JSONDecodeError as exc:
            raise LLMError(f"JSON okunamadı: {blob[:240]}") from exc
    if not isinstance(data, dict):
        raise LLMError("Model bir JSON nesnesi döndürmedi.")
    return data
