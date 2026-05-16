from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from core.db.enums import Language, SpamCategory, ThreatLevel


class PredictionRequest(BaseModel):
    message_text: str = Field(min_length=1, max_length=10000)
    language: Language | None = None


class FeatureContribution(BaseModel):
    feature: str
    score: float
    weight: float


class PredictionResponse(BaseModel):
    id: UUID
    threat_level: ThreatLevel
    spam_category: SpamCategory | None
    confidence_score: float
    language: Language
    explanation: str | None
    contributions: list[FeatureContribution]
    processing_time_ms: int | None
    model_version: str | None


class ModelVersionListItem(BaseModel):
    id: UUID
    name: str
    version: str
    is_active: bool
    deployed_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class ModelVersionDetail(ModelVersionListItem):
    description: str | None
    metrics: dict[str, float] | None


class FeedbackRequest(BaseModel):
    prediction_id: UUID
    is_correct: bool
    correct_label: str | None = Field(default=None, max_length=32)
    notes: str | None = Field(default=None, max_length=2000)


class FeedbackResponse(BaseModel):
    id: UUID
    prediction_id: UUID
    reviewer_id: UUID
    is_correct: bool
    correct_label: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class ModelMetricsResponse(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    total_predictions: int
    total_feedback: int
    false_positive_rate: float
    false_negative_rate: float
