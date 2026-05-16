from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db.base import Base, TimestampMixin, UUIDPKMixin
from core.db.enums import Language, SpamCategory, ThreatLevel


class AIModelVersionModel(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "ai_model_versions"

    name: Mapped[str] = mapped_column(String(128), nullable=False)
    version: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    metrics: Mapped[str | None] = mapped_column(Text, nullable=True)
    deployed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    predictions: Mapped[list["AIPredictionModel"]] = relationship(back_populates="model_version")


class AIPredictionModel(UUIDPKMixin, Base):
    __tablename__ = "ai_predictions"

    message_text: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[Language] = mapped_column(String(16), nullable=False, default=Language.UNKNOWN)
    threat_level: Mapped[ThreatLevel] = mapped_column(String(16), nullable=False, index=True)
    spam_category: Mapped[SpamCategory | None] = mapped_column(String(32), nullable=True)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False)
    model_version_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("ai_model_versions.id", ondelete="SET NULL"), nullable=True
    )
    contributions: Mapped[str | None] = mapped_column(Text, nullable=True)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    processing_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    model_version: Mapped["AIModelVersionModel | None"] = relationship(back_populates="predictions")
    feedback: Mapped[list["AIFeedbackModel"]] = relationship(back_populates="prediction")


class AIFeedbackModel(UUIDPKMixin, Base):
    __tablename__ = "ai_feedback"

    prediction_id: Mapped[UUID] = mapped_column(
        ForeignKey("ai_predictions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    reviewer_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    correct_label: Mapped[SpamCategory | None] = mapped_column(String(32), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    prediction: Mapped["AIPredictionModel"] = relationship(back_populates="feedback")
