from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    telegram_bot_token: str

    # Webhook
    use_webhook: bool = False
    webhook_url: str = ""
    webhook_path: str = "/webhook"
    webhook_secret: str = ""
    webhook_port: int = 8080

    # API Backend
    api_base_url: str = "http://localhost:8000/api/v1"
    api_service_token: str = ""

    # Redis (for FSM storage)
    redis_url: str = "redis://localhost:6379/1"

    # Localization
    default_language: str = "uz_lat"

    # Moderation
    spam_confidence_threshold: float = 0.80
    suspicious_threshold: float = 0.60


@lru_cache(maxsize=1)
def get_bot_settings() -> BotSettings:
    return BotSettings()
