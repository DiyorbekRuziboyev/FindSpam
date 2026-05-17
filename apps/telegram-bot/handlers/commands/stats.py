from __future__ import annotations

from typing import Any

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from filters.chat import IsGroupMessage
from services.group_service import GroupService

router = Router()


@router.message(Command("stats"), IsGroupMessage())
async def cmd_stats(message: Message, **data: Any) -> None:
    from core.api_client import FindSpamAPIClient
    from redis.asyncio import Redis

    redis: Redis = data["redis"]
    api_client: FindSpamAPIClient = data["api_client"]

    svc = GroupService(redis=redis, api_client=api_client)
    stats = await svc.get_stats(message.chat.id)

    if not stats:
        await message.answer("📊 Statistika hali mavjud emas.")
        return

    total_messages = stats.get("total_messages", 0)
    spam_detected = stats.get("spam_detected", 0)
    spam_deleted = stats.get("spam_deleted", 0)
    users_warned = stats.get("users_warned", 0)
    users_banned = stats.get("users_banned", 0)
    spam_rate = round((spam_detected / total_messages * 100) if total_messages else 0, 1)

    text = (
        f"📊 <b>{message.chat.title} — Statistika</b>\n\n"
        f"📨 Jami xabarlar: <b>{total_messages:,}</b>\n"
        f"🚫 Spam aniqlandi: <b>{spam_detected:,}</b>\n"
        f"🗑 O'chirildi: <b>{spam_deleted:,}</b>\n"
        f"⚠️ Ogohlantirishlar: <b>{users_warned:,}</b>\n"
        f"🔒 Bloklashlar: <b>{users_banned:,}</b>\n"
        f"📈 Spam ulushi: <b>{spam_rate}%</b>"
    )
    await message.answer(text)
