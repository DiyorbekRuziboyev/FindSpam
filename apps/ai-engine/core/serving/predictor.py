from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ThreatLevel(StrEnum):
    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class SpamCategory(StrEnum):
    SCAM = "SCAM"
    PHISHING = "PHISHING"
    ADVERTISEMENT = "ADVERTISEMENT"
    FAKE_GIVEAWAY = "FAKE_GIVEAWAY"
    SOCIAL_ENGINEERING = "SOCIAL_ENGINEERING"
    SUSPICIOUS_URL = "SUSPICIOUS_URL"
    OTHER = "OTHER"


@dataclass
class ModelContributions:
    xlm_roberta: float
    mbert: float
    tfidf_lr: float
    rule_engine: float


@dataclass
class PredictionResult:
    is_spam: bool
    confidence: float
    threat_level: ThreatLevel
    spam_category: SpamCategory | None
    model_contributions: ModelContributions
    explanation: dict
    processing_ms: float


class Predictor:
    """
    Ensemble predictor interface. Concrete implementation added in Phase 2.
    Orchestrates: preprocessor → feature extraction → ensemble → explainability.
    """

    async def predict(self, text: str, metadata: dict) -> PredictionResult:
        raise NotImplementedError

    async def predict_batch(
        self, texts: list[str], metadata: list[dict]
    ) -> list[PredictionResult]:
        raise NotImplementedError
