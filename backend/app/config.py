from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = BACKEND_DIR.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(REPO_DIR / ".env"),
        extra="ignore",
    )

    admin_secret: str = ""

    # Owner-paid providers. Fill only the one(s) you have.
    opencode_api_key: str = ""
    openrouter_api_key: str = ""
    gemini_api_key: str = ""

    # Defaults; the admin panel can override and persist these.
    llm_provider: str = "opencode-go"
    llm_model: str = ""

    # Sent to OpenRouter for dashboard attribution (optional).
    public_site_url: str = "http://localhost:3000"
    public_site_name: str = "Hazirlik Prep"

    database_url: str = "sqlite:///./storage/hazirlik.db"
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    explain_rate_limit_per_hour: int = 20
    evaluation_rate_limit_per_hour: int = 30
    coach_rate_limit_per_hour: int = 80
    transcribe_rate_limit_per_hour: int = 30
    whisper_model: str = "base.en"
    whisper_device: str = "cpu"
    whisper_compute_type: str = "int8"
    max_speaking_audio_mb: int = 25
    storage_dir: Path = BACKEND_DIR / "storage"
    content_dir: Path = REPO_DIR / "content"


settings = Settings()
settings.storage_dir.mkdir(parents=True, exist_ok=True)
(settings.storage_dir / "audio").mkdir(parents=True, exist_ok=True)
(settings.storage_dir / "models").mkdir(parents=True, exist_ok=True)
(settings.storage_dir / "transient").mkdir(parents=True, exist_ok=True)
