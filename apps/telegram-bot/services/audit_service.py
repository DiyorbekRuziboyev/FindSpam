from __future__ import annotations

import structlog

from core.api_client import FindSpamAPIClient
from core.event_bus import EventBus

logger = structlog.get_logger(__name__)


class AuditService:
    """Posts structured moderation audit records to the backend API and event bus."""

    def __init__(self, api_client: FindSpamAPIClient, event_bus: EventBus) -> None:
        self._api = api_client
        self._bus = event_bus

    async def record_moderation(
        self,
        chat_id: int,
        user_id: int,
        message_id: int,
        message_text: str,
        action_taken: str,
        threat_level: str,
        spam_category: str | None,
        confidence_score: float,
        reason: str = "",
    ) -> None:
        payload = {
            "telegram_group_id": chat_id,
            "telegram_user_id": user_id,
            "message_id": message_id,
            "message_text": message_text[:2000],
            "action_taken": action_taken,
            "threat_level": threat_level,
            "spam_category": spam_category,
            "confidence_score": confidence_score,
            "reason": reason,
        }
        try:
            await self._api.log_moderation_event(payload)
        except Exception:
            logger.exception(
                "audit_api_failed",
                chat_id=chat_id,
                user_id=user_id,
                action=action_taken,
            )

        await self._bus.publish_spam_detected(
            chat_id=chat_id,
            user_id=user_id,
            message_id=message_id,
            confidence=confidence_score,
            threat_level=threat_level,
            spam_category=spam_category,
            action_taken=action_taken,
        )
