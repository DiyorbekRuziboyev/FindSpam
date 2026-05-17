from __future__ import annotations

import structlog
from redis.asyncio import Redis

logger = structlog.get_logger(__name__)


class FloodDetector:
    """Redis-backed per-user flood detection.

    Fast path evaluated before the AI inference call.
    Key pattern: flood:{chat_id}:{user_id}
    """

    def __init__(self, redis: Redis, threshold: int = 5, window: int = 60) -> None:
        self._redis = redis
        self._threshold = threshold
        self._window = window

    async def check(self, chat_id: int, user_id: int) -> bool:
        """Returns True if the user has exceeded the flood threshold in this window."""
        key = f"flood:{chat_id}:{user_id}"
        try:
            count = await self._redis.incr(key)
            if count == 1:
                await self._redis.expire(key, self._window)
            if count > self._threshold:
                logger.warning(
                    "flood_detected",
                    chat_id=chat_id,
                    user_id=user_id,
                    count=count,
                    threshold=self._threshold,
                )
                return True
        except Exception:
            logger.exception("flood_check_redis_error", chat_id=chat_id, user_id=user_id)
        return False

    async def reset(self, chat_id: int, user_id: int) -> None:
        key = f"flood:{chat_id}:{user_id}"
        try:
            await self._redis.delete(key)
        except Exception:
            pass

    async def get_count(self, chat_id: int, user_id: int) -> int:
        key = f"flood:{chat_id}:{user_id}"
        try:
            val = await self._redis.get(key)
            return int(val) if val else 0
        except Exception:
            return 0
