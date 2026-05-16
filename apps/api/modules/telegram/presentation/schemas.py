from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from core.db.enums import BanType


class TelegramGroupListItem(BaseModel):
    id: UUID
    telegram_id: int
    title: str
    username: str | None
    member_count: int
    is_active: bool
    bot_is_admin: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class TelegramGroupDetail(TelegramGroupListItem):
    settings: dict[str, object] | None
    added_by: UUID | None
    updated_at: datetime


class UpdateGroupSettingsRequest(BaseModel):
    is_active: bool | None = None
    settings: dict[str, object] | None = None


class TelegramUserListItem(BaseModel):
    id: UUID
    telegram_id: int
    username: str | None
    first_name: str | None
    last_name: str | None
    is_bot: bool
    spam_score: float
    warning_count: int
    is_banned: bool
    ban_type: BanType | None
    last_seen_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class TelegramUserDetail(TelegramUserListItem):
    ban_reason: str | None
    banned_until: datetime | None
    updated_at: datetime


class BanUserRequest(BaseModel):
    ban_type: BanType
    reason: str = Field(min_length=5, max_length=500)
    banned_until: datetime | None = None


class UnbanUserRequest(BaseModel):
    reason: str = Field(min_length=5, max_length=500)


class TelegramUserStatsResponse(BaseModel):
    total_users: int
    banned_users: int
    bot_accounts: int
    high_risk_users: int
    avg_spam_score: float
