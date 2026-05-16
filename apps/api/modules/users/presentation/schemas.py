from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from core.db.enums import UserRole


class UserListItem(BaseModel):
    id: UUID
    email: str
    username: str
    role: UserRole
    is_active: bool
    is_verified: bool
    last_login_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class UserDetail(UserListItem):
    updated_at: datetime
    deleted_at: datetime | None


class UpdateUserRequest(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=64)
    role: UserRole | None = None
    is_active: bool | None = None


class CreateUserRequest(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=8, max_length=128)
    role: UserRole = UserRole.MODERATOR


class UserStatsResponse(BaseModel):
    total_users: int
    active_users: int
    verified_users: int
    by_role: dict[str, int]
