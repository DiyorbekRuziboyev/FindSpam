import secrets
from datetime import UTC, datetime, timedelta
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from core.config.settings import get_settings
from core.db.enums import SecurityEventType, SecuritySeverity
from core.exceptions.base import UnauthorizedError
from core.security.jwt import create_access_token
from modules.auth.application.dtos import AuthTokensDTO, RefreshTokenCommand
from modules.auth.infrastructure.models import RefreshTokenModel
from modules.auth.infrastructure.repository import (
    RefreshTokenRepository,
    SecurityEventRepository,
    UserRepository,
)

settings = get_settings()


class RefreshTokenUseCase:
    def __init__(self, session: AsyncSession) -> None:
        self._users = UserRepository(session)
        self._tokens = RefreshTokenRepository(session)
        self._events = SecurityEventRepository(session)

    async def execute(self, command: RefreshTokenCommand) -> AuthTokensDTO:
        token_model = await self._tokens.get_by_token(command.refresh_token)

        if token_model is None:
            raise UnauthorizedError(message="Invalid refresh token")

        if token_model.is_revoked:
            # Token reuse detected — revoke entire family (token theft signal)
            await self._tokens.revoke_family(
                token_model.family_id, reason="reuse_detected"
            )
            await self._events.log(
                SecurityEventType.TOKEN_REUSE_DETECTED,
                SecuritySeverity.CRITICAL,
                user_id=token_model.user_id,
                ip_address=command.ip_address,
                user_agent=command.user_agent,
            )
            raise UnauthorizedError(message="Token reuse detected — all sessions invalidated")

        if token_model.is_expired:
            await self._tokens.revoke_token(token_model.id, reason="expired")
            raise UnauthorizedError(message="Refresh token has expired")

        user = await self._users.get_active_by_id(token_model.user_id)
        if user is None:
            raise UnauthorizedError(message="User account is disabled")

        await self._tokens.revoke_token(token_model.id, reason="rotated")

        access_token = create_access_token({
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
        })

        raw_refresh = secrets.token_urlsafe(48)
        new_token_hash = RefreshTokenRepository.hash_token(raw_refresh)
        expires_at = datetime.now(UTC) + timedelta(days=settings.jwt_refresh_token_expire_days)

        new_refresh_model = RefreshTokenModel(
            token_hash=new_token_hash,
            family_id=token_model.family_id,
            user_id=user.id,
            expires_at=expires_at,
            ip_address=command.ip_address,
            user_agent=command.user_agent,
            created_at=datetime.now(UTC),
        )
        await self._tokens.save(new_refresh_model)

        await self._events.log(
            SecurityEventType.TOKEN_REFRESH,
            SecuritySeverity.INFO,
            user_id=user.id,
            ip_address=command.ip_address,
            user_agent=command.user_agent,
        )

        return AuthTokensDTO(access_token=access_token, refresh_token=raw_refresh)
