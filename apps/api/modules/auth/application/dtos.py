from dataclasses import dataclass
from uuid import UUID

from core.db.enums import UserRole


@dataclass(frozen=True)
class AuthTokensDTO:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


@dataclass(frozen=True)
class UserDTO:
    id: UUID
    email: str
    username: str
    role: UserRole
    is_active: bool
    is_verified: bool


@dataclass(frozen=True)
class LoginCommand:
    email: str
    password: str
    ip_address: str | None = None
    user_agent: str | None = None


@dataclass(frozen=True)
class RefreshTokenCommand:
    refresh_token: str
    ip_address: str | None = None
    user_agent: str | None = None


@dataclass(frozen=True)
class LogoutCommand:
    refresh_token: str
    user_id: UUID
