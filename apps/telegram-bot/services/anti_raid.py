from __future__ import annotations

import structlog
from redis.asyncio import Redis

logger = structlog.get_logger(__name__)


class AntiRaidDetector:
    """Redis-backed group join-rate monitor.

    Counts member joins per sliding window and flags potential coordinated raids.
    Key pattern: raid:{chat_id}:joins
    """

    def __init__(self, redis: Redis, threshold: int = 10, window: int = 30) -> None:
        self._redis = redis
        self._threshold = threshold
        self._window = window

    async def check(self, chat_id: int) -> bool:
        """Returns True if the join rate exceeds the raid threshold."""
        key = f"raid:{chat_id}:joins"
        try:
            count = await self._redis.incr(key)
            if count == 1:
                await self._redis.expire(key, self._window)
            if count > self._threshold:
                logger.warning(
                    "raid_detected",
                    chat_id=chat_id,
                    count=count,
                    threshold=self._threshold,
                    window_seconds=self._window,
                )
                return True
        except Exception:
            logger.exception("anti_raid_redis_error", chat_id=chat_id)
        return False

    async def get_join_count(self, chat_id: int) -> int:
        key = f"raid:{chat_id}:joins"
        try:
            val = await self._redis.get(key)
            return int(val) if val else 0
        except Exception:
            return 0
