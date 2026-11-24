"""Environment-backed application settings."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables and an optional .env file."""

    model_config = SettingsConfigDict(
        env_file=BACKEND_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "LinguaAi"
    api_version: str = "v1"
    log_level: str = "INFO"
    cors_origins: str = "http://localhost:5173"
    database_url: str = "postgresql+psycopg://localhost/linguaai"

    @property
    def allowed_origins(self) -> list[str]:
        """Parse the comma-separated CORS origin setting."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings instance."""
    return Settings()
