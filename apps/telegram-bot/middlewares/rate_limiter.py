from __future__ import annotations

from typing import Any, Awaitable, Callable

import structlog
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from redis.asyncio import Redis

logger = structlog.get_logger(__name__)


class RateLimiterMiddleware(BaseMiddleware):
    """Outer middleware: Redis-backed per-user rate limiter.

    Silently drops messages that exceed the configured limit within the window.
    Reads the Redis client from workflow_data["redis"] (injected by lifespan).
    """

    def __init__(self, limit: int = 20, window: int = 60) -> None:
        self._limit = limit
        self._window = window

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if not isinstance(event, Message) or not event.from_user:
            return await handler(event, data)

        redis: Redis | None = data.get("redis")
        if redis is None:
            return await handler(event, data)

        user_id = event.from_user.id
        key = f"rl:{user_id}"
        try:
            count = await redis.incr(key)
            if count == 1:
                await redis.expire(key, self._window)
            if count > self._limit:
                logger.warning(
                    "rate_limit_exceeded",
                    user_id=user_id,
                    chat_id=event.chat.id,
                    count=count,
                    limit=self._limit,
                )
                return None
        except Exception:
            logger.exception("rate_limiter_redis_error", user_id=user_id)

        return await handler(event, data)
