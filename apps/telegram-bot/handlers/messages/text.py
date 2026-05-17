from __future__ import annotations

from typing import Any

import structlog
from aiogram import F, Router
from aiogram.types import Message

from core.api_client import FindSpamAPIClient
from filters.chat import IsGroupMessage
from filters.user import NotBot
from keyboards.inline.moderation import moderation_action_keyboard
from services.flood_detector import FloodDetector
from services.moderation_service import ModerationService

router = Router()
logger = structlog.get_logger(__name__)

_FLOOD_MUTE_SECONDS = 300


@router.message(F.text | F.caption, IsGroupMessage(), NotBot())
async def handle_text_message(
    message: Message,
    spam_prediction: dict | None,
    **data: Any,
) -> None:
    from redis.asyncio import Redis

    redis: Redis = data["redis"]
    api_client: FindSpamAPIClient = data["api_client"]
    settings = data.get("settings")
    bot = data.get("bot") or message.bot
    if bot is None:
        return

    user = message.from_user
    if user is None:
        return

    # Flood check before AI prediction — fast path
    flood_threshold = getattr(settings, "flood_threshold", 5) if settings else 5
    flood_window = getattr(settings, "flood_window", 60) if settings else 60

    flood_detector = FloodDetector(redis=redis, threshold=flood_threshold, window=flood_window)
    if await flood_detector.check(chat_id=message.chat.id, user_id=user.id):
        svc = ModerationService(bot=bot, api_client=api_client)
        await svc.mute_user(
            chat_id=message.chat.id,
            user_id=user.id,
            duration_seconds=_FLOOD_MUTE_SECONDS,
            message_id=message.message_id,
            message_text=message.text or message.caption or "",
            reason="Flood aniqlandi",
            threat_level="HIGH",
        )
        try:
            await message.answer(
                f"🌊 <b>{user.full_name}</b> flood uchun {_FLOOD_MUTE_SECONDS // 60} daqiqaga jim qilindi."
            )
        except Exception:
            pass
        return

    if spam_prediction is None:
        return

    confidence: float = spam_prediction.get("confidence", 0.0)
    is_spam: bool = spam_prediction.get("is_spam", False)
    threat_level: str = spam_prediction.get("threat_level", "NONE")
    spam_category: str | None = spam_prediction.get("spam_category")

    spam_threshold = getattr(settings, "spam_confidence_threshold", 0.80) if settings else 0.80
    suspicious_threshold = getattr(settings, "suspicious_threshold", 0.60) if settings else 0.60

    if not is_spam or confidence < suspicious_threshold:
        return

    svc = ModerationService(bot=bot, api_client=api_client)
    text_content = message.text or message.caption or ""

    logger.info(
        "spam_detected",
        chat_id=message.chat.id,
        user_id=user.id,
        confidence=confidence,
        threat_level=threat_level,
        spam_category=spam_category,
    )

    if threat_level in ("CRITICAL", "HIGH") and confidence >= spam_threshold:
        # Auto-delete and notify admin channel
        await svc.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await svc.warn_user(
            chat_id=message.chat.id,
            user_id=user.id,
            message_id=message.message_id,
            message_text=text_content,
            reason=f"Auto-moderation: {spam_category or 'SPAM'} ({confidence:.0%})",
            threat_level=threat_level,
            spam_category=spam_category,
            confidence_score=confidence,
        )
        try:
            alert = await message.answer(
                f"🚫 Spam xabari o'chirildi.\n"
                f"👤 Foydalanuvchi: <b>{user.full_name}</b>\n"
                f"📊 Ishonch: <b>{confidence:.0%}</b> | Daraja: <b>{threat_level}</b>",
                reply_markup=moderation_action_keyboard(message.message_id, user.id),
            )
        except Exception:
            pass
    elif confidence >= suspicious_threshold:
        # Flag for admin review without auto-deleting
        try:
            await message.answer(
                f"⚠️ Shubhali xabar aniqlandi.\n"
                f"👤 {user.full_name} | 📊 {confidence:.0%} | {threat_level}",
                reply_markup=moderation_action_keyboard(message.message_id, user.id),
            )
        except Exception:
            pass
