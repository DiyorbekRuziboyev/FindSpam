from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class AIEngineSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8001

    model_path: str = "./model_artifacts"
    xlm_roberta_model: str = "xlm-roberta-base"
    mbert_model: str = "bert-base-multilingual-cased"
    max_seq_length: int = 512
    batch_size: int = 32

    # Ensemble weights (must sum to 1.0)
    weight_xlm_roberta: float = 0.40
    weight_mbert: float = 0.25
    weight_tfidf_lr: float = 0.20
    weight_rule_engine: float = 0.15

    # Thresholds
    threshold_spam: float = 0.80
    threshold_suspicious: float = 0.60
    threshold_review: float = 0.30

    redis_url: str = "redis://localhost:6379/0"
    prediction_cache_ttl: int = 3600


@lru_cache(maxsize=1)
def get_ai_settings() -> AIEngineSettings:
    return AIEngineSettings()
