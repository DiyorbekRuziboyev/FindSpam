from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from core.db.enums import ThreatType


class BlacklistEntryListItem(BaseModel):
    id: UUID
    threat_type: ThreatType
    value: str
    is_whitelist: bool
    reason: str | None
    hit_count: int
    expires_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class BlacklistEntryDetail(BlacklistEntryListItem):
    added_by: UUID | None
    updated_at: datetime


class CreateBlacklistEntryRequest(BaseModel):
    threat_type: ThreatType
    value: str = Field(min_length=1, max_length=512)
    is_whitelist: bool = False
    reason: str | None = Field(default=None, max_length=2000)
    expires_at: datetime | None = None


class UpdateBlacklistEntryRequest(BaseModel):
    reason: str | None = Field(default=None, max_length=2000)
    expires_at: datetime | None = None
    is_whitelist: bool | None = None


class BulkCheckRequest(BaseModel):
    entries: list[dict[str, str]] = Field(
        min_length=1,
        max_length=100,
        description="List of {threat_type, value} pairs to check",
    )


class BulkCheckResultItem(BaseModel):
    threat_type: str
    value: str
    is_blacklisted: bool
    is_whitelisted: bool
    entry_id: UUID | None


class BlacklistStatsResponse(BaseModel):
    total_entries: int
    blacklisted: int
    whitelisted: int
    by_threat_type: dict[str, int]
    total_hits: int
    expiring_soon: int
