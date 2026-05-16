from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from core.db.base import Base, TimestampMixin, UUIDPKMixin
from core.db.enums import ThreatType


class BlacklistEntryModel(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "blacklist_entries"
    __table_args__ = (UniqueConstraint("threat_type", "value", name="uq_blacklist_type_value"),)

    threat_type: Mapped[ThreatType] = mapped_column(String(16), nullable=False, index=True)
    value: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    is_whitelist: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    added_by: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    hit_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
