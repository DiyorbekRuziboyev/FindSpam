import json
import logging
from typing import Any

logger = logging.getLogger(__name__)


class InferenceCache:
    def __init__(self, redis_client: Any, ttl: int = 3600) -> None:
        self._redis = redis_client
        self._ttl = ttl

    async def get(self, key: str) -> dict | None:
        try:
            raw = await self._redis.get(key)
            if raw is None:
                return None
            return json.loads(raw)
        except Exception:
            logger.warning("Cache GET failed", extra={"key": key}, exc_info=True)
            return None

    async def set(self, key: str, value: dict) -> None:
        try:
            await self._redis.setex(key, self._ttl, json.dumps(value))
        except Exception:
            logger.warning("Cache SET failed", extra={"key": key}, exc_info=True)

    async def delete(self, key: str) -> None:
        try:
            await self._redis.delete(key)
        except Exception:
            logger.warning("Cache DELETE failed", extra={"key": key}, exc_info=True)
