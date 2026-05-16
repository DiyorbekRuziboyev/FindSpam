from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from core.db.enums import ContentType, ModerationAction, ReviewStatus, SpamCategory, ThreatLevel


class ModerationEventListItem(BaseModel):
    id: UUID
    telegram_group_id: UUID
    telegram_user_id: UUID
    message_id: int
    content_type: ContentType
    threat_level: ThreatLevel
    spam_category: SpamCategory | None
    confidence_score: float | None
    action_taken: ModerationAction
    review_status: ReviewStatus
    created_at: datetime

    model_config = {"from_attributes": True}


class ModerationEventDetail(ModerationEventListItem):
    message_text: str | None
    ai_prediction_id: UUID | None
    reviewed_by: UUID | None
    reviewed_at: datetime | None
    updated_at: datetime


class ReviewActionRequest(BaseModel):
    review_status: ReviewStatus
    notes: str | None = Field(default=None, max_length=1000)


class ModerationQueueItem(BaseModel):
    id: UUID
    telegram_group_id: UUID
    telegram_user_id: UUID
    message_text: str | None
    threat_level: ThreatLevel
    confidence_score: float | None
    created_at: datetime

    model_config = {"from_attributes": True}


class ModerationStatsResponse(BaseModel):
    total_events: int
    pending_review: int
    actions_taken: dict[str, int]
    threat_distribution: dict[str, int]
    avg_confidence: float
