from __future__ import annotations

from typing import Any

import structlog
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from core.api_client import FindSpamAPIClient
from filters.admin import IsAdmin
from filters.chat import IsGroupMessage
from services.moderation_service import ModerationService

router = Router()
logger = structlog.get_logger(__name__)

_MUTE_DURATION = 10 * 60       # 10 minutes default
_TEMP_BAN_DURATION = 24 * 3600  # 24 hours default


def _get_target(message: Message) -> tuple[int, str] | None:
    """Extract target user ID and display name from reply or first mention."""
    if message.reply_to_message and message.reply_to_message.from_user:
        u = message.reply_to_message.from_user
        return u.id, u.full_name
    return None


def _extract_reason(message: Message) -> str:
    parts = (message.text or "").split(maxsplit=2)
    return parts[2] if len(parts) >= 3 else "Moderator decision"


@router.message(Command("warn"), IsGroupMessage(), IsAdmin())
async def cmd_warn(message: Message, api_client: FindSpamAPIClient, **data: Any) -> None:
    target = _get_target(message)
    if not target:
        await message.reply("⚠️ Ushbu buyruqni xabarga reply qilib ishlating.")
        return

    user_id, name = target
    reason = _extract_reason(message)
    bot = data.get("bot") or message.bot
    if bot is None:
        return

    svc = ModerationService(bot=bot, api_client=api_client)
    await svc.warn_user(
        chat_id=message.chat.id,
        user_id=user_id,
        message_id=message.message_id,
        message_text="",
        reason=reason,
    )
    await message.answer(
        f"⚠️ <b>{name}</b> ogohlantirish oldi.\n📝 Sabab: {reason}"
    )


@router.message(Command("mute"), IsGroupMessage(), IsAdmin())
async def cmd_mute(message: Message, api_client: FindSpamAPIClient, **data: Any) -> None:
    target = _get_target(message)
    if not target:
        await message.reply("🔇 Ushbu buyruqni xabarga reply qilib ishlating.")
        return

    user_id, name = target
    reason = _extract_reason(message)
    bot = data.get("bot") or message.bot
    if bot is None:
        return

    svc = ModerationService(bot=bot, api_client=api_client)
    success = await svc.mute_user(
        chat_id=message.chat.id,
        user_id=user_id,
        duration_seconds=_MUTE_DURATION,
        message_id=message.message_id,
        reason=reason,
    )
    if success:
        await message.answer(
            f"🔇 <b>{name}</b> 10 daqiqaga jim qilindi.\n📝 Sabab: {reason}"
        )
    else:
        await message.reply("❌ Foydalanuvchini jim qilib bo'lmadi.")


@router.message(Command("unmute"), IsGroupMessage(), IsAdmin())
async def cmd_unmute(message: Message, **data: Any) -> None:
    target = _get_target(message)
    if not target:
        await message.reply("🔊 Ushbu buyruqni xabarga reply qilib ishlating.")
        return

    user_id, name = target
    bot = data.get("bot") or message.bot
    if bot is None:
        return

    from core.api_client import FindSpamAPIClient as _C
    api_client: FindSpamAPIClient = data["api_client"]
    svc = ModerationService(bot=bot, api_client=api_client)
    success = await svc.unmute_user(chat_id=message.chat.id, user_id=user_id)
    if success:
        await message.answer(f"🔊 <b>{name}</b> gapirishga ruxsat berildi.")
    else:
        await message.reply("❌ Foydalanuvchini jim qilishdan chiqarib bo'lmadi.")


@router.message(Command("ban"), IsGroupMessage(), IsAdmin())
async def cmd_ban(message: Message, api_client: FindSpamAPIClient, **data: Any) -> None:
    target = _get_target(message)
    if not target:
        await message.reply("🚫 Ushbu buyruqni xabarga reply qilib ishlating.")
        return

    user_id, name = target
    reason = _extract_reason(message)
    bot = data.get("bot") or message.bot
    if bot is None:
        return

    svc = ModerationService(bot=bot, api_client=api_client)
    success = await svc.permanent_ban_user(
        chat_id=message.chat.id,
        user_id=user_id,
        message_id=message.message_id,
        reason=reason,
    )
    if success:
        await message.answer(
            f"🚫 <b>{name}</b> guruhdan doimiy ravishda bloklandi.\n📝 Sabab: {reason}"
        )
    else:
        await message.reply("❌ Foydalanuvchini bloklash muvaffaqiyatsiz bo'ldi.")


@router.message(Command("unban"), IsGroupMessage(), IsAdmin())
async def cmd_unban(message: Message, api_client: FindSpamAPIClient, **data: Any) -> None:
    target = _get_target(message)
    if not target:
        await message.reply("✅ Ushbu buyruqni xabarga reply qilib ishlating.")
        return

    user_id, name = target
    bot = data.get("bot") or message.bot
    if bot is None:
        return

    svc = ModerationService(bot=bot, api_client=api_client)
    success = await svc.unban_user(chat_id=message.chat.id, user_id=user_id)
    if success:
        await message.answer(f"✅ <b>{name}</b> blokdan chiqarildi.")
    else:
        await message.reply("❌ Foydalanuvchini blokdan chiqarib bo'lmadi.")


@router.message(Command("kick"), IsGroupMessage(), IsAdmin())
async def cmd_kick(message: Message, api_client: FindSpamAPIClient, **data: Any) -> None:
    target = _get_target(message)
    if not target:
        await message.reply("👢 Ushbu buyruqni xabarga reply qilib ishlating.")
        return

    user_id, name = target
    bot = data.get("bot") or message.bot
    if bot is None:
        return

    svc = ModerationService(bot=bot, api_client=api_client)
    success = await svc.kick_user(chat_id=message.chat.id, user_id=user_id)
    if success:
        await message.answer(f"👢 <b>{name}</b> guruhdan haydaldi.")
    else:
        await message.reply("❌ Foydalanuvchini haydab bo'lmadi.")
