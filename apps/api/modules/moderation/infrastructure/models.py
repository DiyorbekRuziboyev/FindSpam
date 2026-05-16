from datetime import datetime
from uuid import UUID

from sqlalchemy import BigInteger, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db.base import Base, TimestampMixin, UUIDPKMixin
from core.db.enums import (
    ContentType,
    ModerationAction,
    ReviewStatus,
    SpamCategory,
    ThreatLevel,
)


class ModerationEventModel(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "moderation_events"

    telegram_group_id: Mapped[UUID] = mapped_column(
        ForeignKey("telegram_groups.id", ondelete="CASCADE"), nullable=False, index=True
    )
    telegram_user_id: Mapped[UUID] = mapped_column(
        ForeignKey("telegram_users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    message_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    message_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    content_type: Mapped[ContentType] = mapped_column(String(16), nullable=False, default=ContentType.TEXT)
    threat_level: Mapped[ThreatLevel] = mapped_column(String(16), nullable=False, index=True)
    spam_category: Mapped[SpamCategory | None] = mapped_column(String(32), nullable=True)
    confidence_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    ai_prediction_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("ai_predictions.id", ondelete="SET NULL"), nullable=True
    )
    action_taken: Mapped[ModerationAction] = mapped_column(String(32), nullable=False, index=True)
    review_status: Mapped[ReviewStatus] = mapped_column(
        String(16), nullable=False, default=ReviewStatus.PENDING, index=True
    )
    reviewed_by: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
