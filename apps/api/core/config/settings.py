from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_env: str = "development"
    app_name: str = "FindSpam"
    app_version: str = "1.0.0"
    debug: bool = False

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_prefix: str = "/api/v1"
    cors_origins: list[str] = ["http://localhost:3000"]

    # Database
    database_url: str

    # Redis
    redis_url: str

    # JWT
    jwt_algorithm: str = "RS256"
    jwt_private_key_path: str = "./infrastructure/keys/private.pem"
    jwt_public_key_path: str = "./infrastructure/keys/public.pem"
    jwt_access_token_expire_minutes: int = 15
    jwt_refresh_token_expire_days: int = 30

    # Telegram
    telegram_bot_token: str
    telegram_webhook_url: str = ""
    telegram_webhook_secret: str = ""

    # AI Engine
    ai_engine_host: str = "localhost"
    ai_engine_port: int = 8001
    ai_confidence_threshold_spam: float = 0.80
    ai_confidence_threshold_suspicious: float = 0.60
    ai_confidence_threshold_review: float = 0.30

    # Rate Limiting
    rate_limit_login_per_15min: int = 5
    rate_limit_api_per_minute: int = 100

    # Logging
    log_level: str = "INFO"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
