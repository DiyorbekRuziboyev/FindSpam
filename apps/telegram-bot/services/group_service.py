from __future__ import annotations

import json

import structlog
from redis.asyncio import Redis

from core.api_client import FindSpamAPIClient

logger = structlog.get_logger(__name__)

_SETTINGS_TTL = 3600
_KEY = "group_settings:{chat_id}"


class GroupService:
    """Group configuration service with Redis-backed settings cache."""

    def __init__(self, redis: Redis, api_client: FindSpamAPIClient) -> None:
        self._redis = redis
        self._api = api_client

    async def get_settings(self, chat_id: int) -> dict:
        key = _KEY.format(chat_id=chat_id)
        try:
            cached = await self._redis.get(key)
            if cached:
                return json.loads(cached)
        except Exception:
            pass

        try:
            settings = await self._api.get_group_settings(chat_id)
        except Exception:
            logger.exception("get_group_settings_api_failed", chat_id=chat_id)
            settings = {}

        if settings:
            try:
                await self._redis.set(key, json.dumps(settings), ex=_SETTINGS_TTL)
            except Exception:
                pass

        return settings

    async def update_settings(self, chat_id: int, updates: dict) -> dict:
        try:
            result = await self._api.update_group_settings(chat_id, updates)
        except Exception:
            logger.exception("update_group_settings_api_failed", chat_id=chat_id)
            return {}

        key = _KEY.format(chat_id=chat_id)
        try:
            await self._redis.delete(key)
        except Exception:
            pass

        return result

    async def get_stats(self, chat_id: int) -> dict:
        try:
            return await self._api.get_group_stats(chat_id)
        except Exception:
            logger.exception("get_group_stats_api_failed", chat_id=chat_id)
            return {}
