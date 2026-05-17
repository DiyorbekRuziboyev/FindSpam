from __future__ import annotations

import json
from datetime import datetime

import structlog
from redis.asyncio import Redis

logger = structlog.get_logger(__name__)

_CHANNEL = "findspam:moderation_events"


class EventBus:
    """Redis pub/sub publisher for real-time moderation events.

    The admin dashboard subscribes to the findspam:moderation_events channel
    and receives events as they happen for live monitoring.
    """

    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def publish(self, event_type: str, payload: dict) -> None:
        message = {
            "event_type": event_type,
            "payload": payload,
            "published_at": datetime.utcnow().isoformat(),
        }
        try:
            await self._redis.publish(_CHANNEL, json.dumps(message, ensure_ascii=False))
        except Exception:
            logger.exception("event_bus_publish_failed", event_type=event_type)

    async def publish_spam_detected(
        self,
        chat_id: int,
        user_id: int,
        message_id: int,
        confidence: float,
        threat_level: str,
        spam_category: str | None,
        action_taken: str,
    ) -> None:
        await self.publish(
            "spam_detected",
            {
                "chat_id": chat_id,
                "user_id": user_id,
                "message_id": message_id,
                "confidence": confidence,
                "threat_level": threat_level,
                "spam_category": spam_category,
                "action_taken": action_taken,
            },
        )

    async def publish_user_action(
        self,
        chat_id: int,
        user_id: int,
        action: str,
        reason: str,
        operator_id: int | None = None,
    ) -> None:
        await self.publish(
            "user_action",
            {
                "chat_id": chat_id,
                "user_id": user_id,
                "action": action,
                "reason": reason,
                "operator_id": operator_id,
            },
        )

    async def publish_raid_alert(self, chat_id: int, join_count: int) -> None:
        await self.publish(
            "raid_alert",
            {"chat_id": chat_id, "join_count": join_count},
        )
