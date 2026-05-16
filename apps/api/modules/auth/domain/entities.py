from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from core.db.enums import SecurityEventType, SecuritySeverity, UserRole


@dataclass
class User:
    id: UUID
    email: str
    username: str
    hashed_password: str
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime | None = None
    deleted_at: datetime | None = None

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None


@dataclass
class RefreshToken:
    id: UUID
    token_hash: str
    family_id: UUID
    user_id: UUID
    expires_at: datetime
    created_at: datetime
    revoked_at: datetime | None = None
    revoked_reason: str | None = None
    ip_address: str | None = None
    user_agent: str | None = None

    @property
    def is_revoked(self) -> bool:
        return self.revoked_at is not None


@dataclass
class SecurityEvent:
    id: UUID
    event_type: SecurityEventType
    severity: SecuritySeverity
    created_at: datetime
    user_id: UUID | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    metadata: dict = field(default_factory=dict)
