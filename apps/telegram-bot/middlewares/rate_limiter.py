from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message


class RateLimiterMiddleware(BaseMiddleware):
    """Redis-backed per-user rate limiter. Implementation in Phase 3."""

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        return await handler(event, data)
