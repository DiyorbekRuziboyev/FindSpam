from __future__ import annotations

import structlog
from aiogram import Bot
from aiogram.types import ChatPermissions

from core.api_client import FindSpamAPIClient

logger = structlog.get_logger(__name__)

_MUTE_PERMISSIONS = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_polls=False,
    can_send_other_messages=False,
    can_add_web_page_previews=False,
)

_FULL_PERMISSIONS = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True,
)


class ModerationService:
    """Orchestrates Telegram moderation actions and persists events to the backend API."""

    def __init__(self, bot: Bot, api_client: FindSpamAPIClient) -> None:
        self._bot = bot
        self._api = api_client

    async def delete_message(self, chat_id: int, message_id: int) -> bool:
        try:
            await self._bot.delete_message(chat_id=chat_id, message_id=message_id)
            return True
        except Exception:
            logger.exception("delete_message_failed", chat_id=chat_id, message_id=message_id)
            return False

    async def warn_user(
        self,
        chat_id: int,
        user_id: int,
        message_id: int,
        message_text: str,
        reason: str,
        threat_level: str = "MEDIUM",
        spam_category: str | None = None,
        confidence_score: float = 0.0,
    ) -> dict:
        payload = {
            "telegram_group_id": chat_id,
            "telegram_user_id": user_id,
            "message_id": message_id,
            "message_text": message_text[:2000],
            "action_taken": "WARN",
            "threat_level": threat_level,
            "spam_category": spam_category,
            "confidence_score": confidence_score,
            "reason": reason,
        }
        try:
            result = await self._api.log_moderation_event(payload)
            logger.info("user_warned", chat_id=chat_id, user_id=user_id)
            return result
        except Exception:
            logger.exception("warn_user_api_failed", chat_id=chat_id, user_id=user_id)
            return {}

    async def mute_user(
        self,
        chat_id: int,
        user_id: int,
        duration_seconds: int,
        message_id: int = 0,
        message_text: str = "",
        reason: str = "",
        threat_level: str = "HIGH",
        confidence_score: float = 0.0,
    ) -> bool:
        import time

        until_date = int(time.time()) + duration_seconds
        try:
            await self._bot.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions=_MUTE_PERMISSIONS,
                until_date=until_date,
            )
        except Exception:
            logger.exception("mute_telegram_failed", chat_id=chat_id, user_id=user_id)
            return False

        payload = {
            "telegram_group_id": chat_id,
            "telegram_user_id": user_id,
            "message_id": message_id,
            "message_text": message_text[:2000],
            "action_taken": "MUTE",
            "threat_level": threat_level,
            "confidence_score": confidence_score,
            "reason": reason,
            "duration_seconds": duration_seconds,
        }
        try:
            await self._api.log_moderation_event(payload)
        except Exception:
            logger.exception("mute_api_log_failed", chat_id=chat_id, user_id=user_id)

        logger.info("user_muted", chat_id=chat_id, user_id=user_id, duration=duration_seconds)
        return True

    async def unmute_user(self, chat_id: int, user_id: int) -> bool:
        try:
            await self._bot.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions=_FULL_PERMISSIONS,
            )
            logger.info("user_unmuted", chat_id=chat_id, user_id=user_id)
            return True
        except Exception:
            logger.exception("unmute_failed", chat_id=chat_id, user_id=user_id)
            return False

    async def temp_ban_user(
        self,
        chat_id: int,
        user_id: int,
        duration_seconds: int,
        message_id: int = 0,
        message_text: str = "",
        reason: str = "",
        threat_level: str = "HIGH",
        confidence_score: float = 0.0,
    ) -> bool:
        import time

        until_date = int(time.time()) + duration_seconds
        try:
            await self._bot.ban_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                until_date=until_date,
                revoke_messages=True,
            )
        except Exception:
            logger.exception("temp_ban_telegram_failed", chat_id=chat_id, user_id=user_id)
            return False

        payload = {
            "telegram_group_id": chat_id,
            "telegram_user_id": user_id,
            "message_id": message_id,
            "message_text": message_text[:2000],
            "action_taken": "TEMP_BAN",
            "threat_level": threat_level,
            "confidence_score": confidence_score,
            "reason": reason,
            "duration_seconds": duration_seconds,
        }
        try:
            await self._api.log_moderation_event(payload)
        except Exception:
            logger.exception("temp_ban_api_log_failed", chat_id=chat_id, user_id=user_id)

        logger.info("user_temp_banned", chat_id=chat_id, user_id=user_id, duration=duration_seconds)
        return True

    async def permanent_ban_user(
        self,
        chat_id: int,
        user_id: int,
        message_id: int = 0,
        message_text: str = "",
        reason: str = "",
        threat_level: str = "CRITICAL",
        confidence_score: float = 0.0,
    ) -> bool:
        try:
            await self._bot.ban_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                revoke_messages=True,
            )
        except Exception:
            logger.exception("permanent_ban_telegram_failed", chat_id=chat_id, user_id=user_id)
            return False

        payload = {
            "telegram_group_id": chat_id,
            "telegram_user_id": user_id,
            "message_id": message_id,
            "message_text": message_text[:2000],
            "action_taken": "PERMANENT_BAN",
            "threat_level": threat_level,
            "confidence_score": confidence_score,
            "reason": reason,
        }
        try:
            await self._api.log_moderation_event(payload)
        except Exception:
            logger.exception("permanent_ban_api_log_failed", chat_id=chat_id, user_id=user_id)

        logger.info("user_permanently_banned", chat_id=chat_id, user_id=user_id)
        return True

    async def unban_user(self, chat_id: int, user_id: int) -> bool:
        try:
            await self._bot.unban_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                only_if_banned=True,
            )
            logger.info("user_unbanned", chat_id=chat_id, user_id=user_id)
            return True
        except Exception:
            logger.exception("unban_failed", chat_id=chat_id, user_id=user_id)
            return False

    async def kick_user(self, chat_id: int, user_id: int) -> bool:
        """Kick without permanent ban — unban immediately after to allow rejoining."""
        try:
            await self._bot.ban_chat_member(chat_id=chat_id, user_id=user_id)
            await self._bot.unban_chat_member(chat_id=chat_id, user_id=user_id)
            logger.info("user_kicked", chat_id=chat_id, user_id=user_id)
            return True
        except Exception:
            logger.exception("kick_failed", chat_id=chat_id, user_id=user_id)
            return False
