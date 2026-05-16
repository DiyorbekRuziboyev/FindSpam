from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from core.db.base import Base, UUIDPKMixin


class AnalyticsSnapshotModel(UUIDPKMixin, Base):
    __tablename__ = "analytics_snapshots"
    __table_args__ = (UniqueConstraint("snapshot_date"),)

    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    total_messages: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    spam_detected: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    scam_detected: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    phishing_detected: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    clean_messages: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    avg_confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    total_bans: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_warnings: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_deletions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    by_language: Mapped[str | None] = mapped_column(Text, nullable=True)
    by_category: Mapped[str | None] = mapped_column(Text, nullable=True)
    by_threat_level: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
