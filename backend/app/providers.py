"""Provider presets.

The site owner pays for the models. Visitors never send a key.
Everything is configured with one env var per provider plus a model
chosen from a dropdown in the admin panel.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .config import settings


# Keys entered from the admin panel. Persisted in the settings table and
# reloaded on startup, so the owner never has to edit .env by hand.
_panel_keys: dict[str, str] = {}

KEY_ENVS = ("OPENCODE_API_KEY", "OPENROUTER_API_KEY", "GEMINI_API_KEY")


def set_panel_key(key_env: str, value: str) -> None:
    if value:
        _panel_keys[key_env] = value
    else:
        _panel_keys.pop(key_env, None)


def panel_key(key_env: str) -> str:
    return _panel_keys.get(key_env, "")


def env_key(key_env: str) -> str:
    return str(getattr(settings, key_env.lower(), "") or "")


def mask_key(value: str) -> str:
    if not value:
        return ""
    if len(value) <= 10:
        return f"{value[:2]}…{value[-2:]}"
    return f"{value[:6]}…{value[-4:]}"


@dataclass(frozen=True)
class Provider:
    id: str
    label: str
    note: str
    base_url: str
    key_env: str
    models_path: str = "/models"
    # substrings used to float good general-purpose models to the top
    prefer: tuple[str, ...] = field(default=())

    @property
    def api_key(self) -> str:
        return panel_key(self.key_env) or env_key(self.key_env)

    @property
    def key_source(self) -> str:
        if panel_key(self.key_env):
            return "panel"
        if env_key(self.key_env):
            return "env"
        return "none"

    @property
    def configured(self) -> bool:
        return bool(self.api_key)


PROVIDERS: dict[str, Provider] = {
    "opencode-go": Provider(
        id="opencode-go",
        label="OpenCode Go",
        note="Aylık abonelik. Açık kaynak modeller (Grok, GLM, Kimi, DeepSeek).",
        base_url="https://opencode.ai/zen/go/v1",
        key_env="OPENCODE_API_KEY",
        prefer=("grok", "glm", "kimi", "deepseek", "qwen", "minimax"),
    ),
    "opencode-zen": Provider(
        id="opencode-zen",
        label="OpenCode Zen",
        note="Kullandıkça öde. Tüm katalog: GPT, Claude, Gemini ve açık modeller.",
        base_url="https://opencode.ai/zen/v1",
        key_env="OPENCODE_API_KEY",
        prefer=("claude", "gpt", "gemini", "deepseek", "glm", "kimi", "grok"),
    ),
    "openrouter": Provider(
        id="openrouter",
        label="OpenRouter",
        note="Bakiyeni kullanır. 400+ model, tek anahtar.",
        base_url="https://openrouter.ai/api/v1",
        key_env="OPENROUTER_API_KEY",
        prefer=("claude", "gpt", "gemini", "deepseek", "grok", "glm", "qwen", "llama"),
    ),
    "gemini": Provider(
        id="gemini",
        label="Google Gemini",
        note="Yedek. Ücretsiz kotası var, kalite daha düşük.",
        base_url="https://generativelanguage.googleapis.com/v1beta",
        key_env="GEMINI_API_KEY",
        prefer=("flash", "pro"),
    ),
}

DEFAULT_ORDER = ("opencode-go", "openrouter", "opencode-zen", "gemini")


def get_provider(provider_id: str) -> Provider | None:
    return PROVIDERS.get(provider_id)


def first_configured() -> Provider | None:
    for pid in DEFAULT_ORDER:
        p = PROVIDERS[pid]
        if p.configured:
            return p
    return None


def rank_models(provider: Provider, ids: list[str]) -> list[str]:
    """Put generally strong, non-specialised models first."""

    noisy = ("embed", "whisper", "tts", "image", "vision-only", "rerank", "moderation", "free-test")

    def score(model_id: str) -> tuple[int, int, str]:
        low = model_id.lower()
        penalty = 1 if any(n in low for n in noisy) else 0
        pref = len(provider.prefer)
        for i, token in enumerate(provider.prefer):
            if token in low:
                pref = i
                break
        return (penalty, pref, low)

    return sorted(dict.fromkeys(ids), key=score)
