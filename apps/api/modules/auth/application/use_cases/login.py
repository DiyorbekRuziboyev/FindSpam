import os
import secrets
from datetime import UTC, datetime, timedelta
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from core.config.settings import get_settings
from core.db.enums import SecurityEventType, SecuritySeverity
from core.exceptions.base import UnauthorizedError
from core.security.jwt import create_access_token
from core.security.password import verify_password
from modules.auth.application.dtos import AuthTokensDTO, LoginCommand
from modules.auth.infrastructure.models import RefreshTokenModel
from modules.auth.infrastructure.repository import (
    RefreshTokenRepository,
    SecurityEventRepository,
    UserRepository,
)

settings = get_settings()


class LoginUseCase:
    def __init__(self, session: AsyncSession) -> None:
        self._users = UserRepository(session)
        self._tokens = RefreshTokenRepository(session)
        self._events = SecurityEventRepository(session)

    async def execute(self, command: LoginCommand) -> AuthTokensDTO:
        user = await self._users.get_by_email(command.email)

        if user is None or not verify_password(command.password, user.hashed_password):
            await self._events.log(
                SecurityEventType.LOGIN_FAILURE,
                SecuritySeverity.WARNING,
                ip_address=command.ip_address,
                user_agent=command.user_agent,
            )
            raise UnauthorizedError(message="Invalid email or password")

        if not user.is_active or user.is_deleted:
            raise UnauthorizedError(message="Account is disabled")

        await self._users.update_last_login(user.id)

        access_token = create_access_token({
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
        })

        raw_refresh = secrets.token_urlsafe(48)
        token_hash = RefreshTokenRepository.hash_token(raw_refresh)
        family_id = uuid4()
        expires_at = datetime.now(UTC) + timedelta(days=settings.jwt_refresh_token_expire_days)

        refresh_model = RefreshTokenModel(
            token_hash=token_hash,
            family_id=family_id,
            user_id=user.id,
            expires_at=expires_at,
            ip_address=command.ip_address,
            user_agent=command.user_agent,
            created_at=datetime.now(UTC),
        )
        await self._tokens.save(refresh_model)

        await self._events.log(
            SecurityEventType.LOGIN_SUCCESS,
            SecuritySeverity.INFO,
            user_id=user.id,
            ip_address=command.ip_address,
            user_agent=command.user_agent,
        )

        return AuthTokensDTO(access_token=access_token, refresh_token=raw_refresh)
