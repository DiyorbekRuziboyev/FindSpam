from __future__ import annotations

from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000)
    metadata: dict = Field(default_factory=dict)


class ModelContributionsSchema(BaseModel):
    xlm_roberta: float
    mbert: float
    tfidf_lr: float
    rule_engine: float


class PredictResponse(BaseModel):
    is_spam: bool
    confidence: float = Field(..., ge=0.0, le=1.0)
    threat_level: str
    spam_category: str | None
    model_contributions: ModelContributionsSchema
    explanation: dict
    processing_ms: float


class BatchPredictRequest(BaseModel):
    texts: list[str] = Field(..., min_length=1, max_length=100)
    metadata: list[dict] | None = None


class BatchPredictResponse(BaseModel):
    results: list[PredictResponse | None]
    total_ms: float
    failed_count: int


class FeedbackRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000)
    predicted_spam: bool
    is_spam: bool
    confidence: float = Field(..., ge=0.0, le=1.0)
    source: str = "user"


class HealthResponse(BaseModel):
    status: str
    service: str
    models_loaded: dict[str, bool]
    version: str
