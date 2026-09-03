from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = BACKEND_DIR.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(REPO_DIR / ".env"),
        extra="ignore",
    )

    app_env: str = "development"
    railway_environment: str = ""
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
    akis_chat_rate_limit_per_hour: int = 60
    transcribe_rate_limit_per_hour: int = 30
    ai_daily_request_limit: int = 250
    transcribe_daily_request_limit: int = 100
    turnstile_rate_limit_per_hour: int = 30
    turnstile_daily_request_limit: int = 1000
    ai_max_concurrent: int = 3
    transcribe_max_concurrent: int = 1
    rate_limit_hash_secret: str = ""
    turnstile_site_key: str = ""
    turnstile_secret_key: str = ""
    turnstile_session_secret: str = ""
    turnstile_session_minutes: int = 30
    turnstile_allowed_hostnames: str = ""
    resend_api_key: str = ""
    contact_to_email: str = ""
    contact_from_email: str = "Ankara Hazırlık <onboarding@resend.dev>"
    contact_rate_limit_per_hour: int = 5
    contact_daily_request_limit: int = 100
    whisper_model: str = "base.en"
    whisper_device: str = "cpu"
    whisper_compute_type: str = "int8"
    whisper_beam_size: int = 1
    whisper_worker_timeout_seconds: int = 180
    max_speaking_audio_mb: int = 25
    akis_pack_size: int = 5
    storage_dir: Path = BACKEND_DIR / "storage"
    content_dir: Path = REPO_DIR / "content"

    @property
    def is_production(self) -> bool:
        return self.app_env.strip().lower() == "production" or bool(self.railway_environment.strip())

    @property
    def admin_key_management_enabled(self) -> bool:
        return not self.is_production

    @property
    def turnstile_enabled(self) -> bool:
        return bool(self.turnstile_site_key.strip() and self.turnstile_secret_key.strip())

    @property
    def contact_enabled(self) -> bool:
        return bool(self.resend_api_key.strip() and self.contact_to_email.strip() and self.contact_from_email.strip())


settings = Settings()
settings.storage_dir.mkdir(parents=True, exist_ok=True)
(settings.storage_dir / "audio").mkdir(parents=True, exist_ok=True)
(settings.storage_dir / "models").mkdir(parents=True, exist_ok=True)
(settings.storage_dir / "transient").mkdir(parents=True, exist_ok=True)
