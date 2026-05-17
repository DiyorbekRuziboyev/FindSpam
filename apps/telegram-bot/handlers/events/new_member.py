from __future__ import annotations

from typing import Any

import structlog
from aiogram import Router
from aiogram.types import ChatMemberUpdated

from services.anti_raid import AntiRaidDetector

router = Router()
logger = structlog.get_logger(__name__)


@router.chat_member()
async def handle_member_update(event: ChatMemberUpdated, **data: Any) -> None:
    from aiogram.types import ChatMemberMember, ChatMemberRestricted
    from redis.asyncio import Redis

    # Only react to new member joins
    new_status = event.new_chat_member
    if not isinstance(new_status, (ChatMemberMember, ChatMemberRestricted)):
        return

    old_status = event.old_chat_member
    # Must be a transition from non-member state
    from aiogram.types import ChatMemberLeft, ChatMemberBanned
    if isinstance(old_status, (ChatMemberMember, ChatMemberRestricted)):
        return

    redis: Redis = data["redis"]
    settings = data.get("settings")
    bot = data.get("bot")

    raid_threshold = getattr(settings, "raid_join_threshold", 10) if settings else 10
    raid_window = getattr(settings, "raid_window", 30) if settings else 30

    anti_raid = AntiRaidDetector(redis=redis, threshold=raid_threshold, window=raid_window)
    is_raid = await anti_raid.check(chat_id=event.chat.id)

    if is_raid and bot is not None:
        join_count = await anti_raid.get_join_count(event.chat.id)
        logger.warning(
            "raid_alert_sent",
            chat_id=event.chat.id,
            join_count=join_count,
        )
        try:
            await bot.send_message(
                chat_id=event.chat.id,
                text=(
                    f"🚨 <b>RAID XAVFI!</b>\n\n"
                    f"So'nggi {raid_window}s ichida <b>{join_count}</b> ta yangi a'zo qo'shildi.\n"
                    "Adminlar e'tibor bering!"
                ),
            )
        except Exception:
            logger.exception("raid_alert_send_failed", chat_id=event.chat.id)
