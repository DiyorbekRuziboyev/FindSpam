import hashlib
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.enums import SecurityEventType, SecuritySeverity
from core.repository.base import SQLAlchemyRepository
from modules.auth.infrastructure.models import (
    RefreshTokenModel,
    SecurityEventModel,
    UserModel,
)


class UserRepository(SQLAlchemyRepository[UserModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, UserModel)

    async def get_by_email(self, email: str) -> UserModel | None:
        return await self.get_by(email=email)

    async def get_by_username(self, username: str) -> UserModel | None:
        return await self.get_by(username=username)

    async def get_active_by_id(self, user_id: UUID) -> UserModel | None:
        stmt = (
            select(UserModel)
            .where(UserModel.id == user_id)
            .where(UserModel.is_active.is_(True))
            .where(UserModel.deleted_at.is_(None))
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_last_login(self, user_id: UUID) -> None:
        await self._session.execute(
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(last_login_at=datetime.now(UTC))
        )


class RefreshTokenRepository(SQLAlchemyRepository[RefreshTokenModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, RefreshTokenModel)

    @staticmethod
    def hash_token(raw_token: str) -> str:
        return hashlib.sha256(raw_token.encode()).hexdigest()

    async def get_by_token(self, raw_token: str) -> RefreshTokenModel | None:
        token_hash = self.hash_token(raw_token)
        return await self.get_by(token_hash=token_hash)

    async def revoke_family(self, family_id: UUID, reason: str) -> None:
        now = datetime.now(UTC)
        await self._session.execute(
            update(RefreshTokenModel)
            .where(RefreshTokenModel.family_id == family_id)
            .where(RefreshTokenModel.revoked_at.is_(None))
            .values(revoked_at=now, revoked_reason=reason)
        )

    async def revoke_token(self, token_id: UUID, reason: str) -> None:
        now = datetime.now(UTC)
        await self._session.execute(
            update(RefreshTokenModel)
            .where(RefreshTokenModel.id == token_id)
            .values(revoked_at=now, revoked_reason=reason)
        )

    async def revoke_all_for_user(self, user_id: UUID) -> None:
        now = datetime.now(UTC)
        await self._session.execute(
            update(RefreshTokenModel)
            .where(RefreshTokenModel.user_id == user_id)
            .where(RefreshTokenModel.revoked_at.is_(None))
            .values(revoked_at=now, revoked_reason="logout_all")
        )


class SecurityEventRepository(SQLAlchemyRepository[SecurityEventModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, SecurityEventModel)

    async def log(
        self,
        event_type: SecurityEventType,
        severity: SecuritySeverity,
        user_id: UUID | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> SecurityEventModel:
        event = SecurityEventModel(
            user_id=user_id,
            event_type=event_type,
            severity=severity,
            ip_address=ip_address,
            user_agent=user_agent,
            created_at=datetime.now(UTC),
        )
        return await self.save(event)
