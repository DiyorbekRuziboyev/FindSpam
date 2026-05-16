from sqlalchemy.ext.asyncio import AsyncSession

from core.db.enums import SecurityEventType, SecuritySeverity
from core.exceptions.base import UnauthorizedError
from modules.auth.application.dtos import LogoutCommand
from modules.auth.infrastructure.repository import (
    RefreshTokenRepository,
    SecurityEventRepository,
)


class LogoutUseCase:
    def __init__(self, session: AsyncSession) -> None:
        self._tokens = RefreshTokenRepository(session)
        self._events = SecurityEventRepository(session)

    async def execute(self, command: LogoutCommand) -> None:
        token_model = await self._tokens.get_by_token(command.refresh_token)

        if token_model is None or token_model.user_id != command.user_id:
            raise UnauthorizedError(message="Invalid refresh token")

        if not token_model.is_revoked:
            await self._tokens.revoke_token(token_model.id, reason="logout")

        await self._events.log(
            SecurityEventType.LOGOUT,
            SecuritySeverity.INFO,
            user_id=command.user_id,
        )
