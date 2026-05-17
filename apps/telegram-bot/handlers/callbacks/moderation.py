from __future__ import annotations

from typing import Any

import structlog
from aiogram import F, Router
from aiogram.types import CallbackQuery

from core.api_client import FindSpamAPIClient
from services.moderation_service import ModerationService

router = Router()
logger = structlog.get_logger(__name__)

_BAN_MUTE_DURATION = 24 * 3600  # 24 hours for callback-triggered mute


@router.callback_query(F.data.startswith("mod:"))
async def handle_moderation_callback(callback: CallbackQuery, **data: Any) -> None:
    if callback.data is None or callback.message is None:
        await callback.answer()
        return

    parts = callback.data.split(":")
    if len(parts) < 4:
        await callback.answer("❌ Noto'g'ri buyruq.")
        return

    action = parts[1]
    message_id = int(parts[2])
    user_id = int(parts[3])

    api_client: FindSpamAPIClient = data["api_client"]
    bot = data.get("bot") or callback.bot
    if bot is None:
        await callback.answer()
        return

    chat_id = callback.message.chat.id
    svc = ModerationService(bot=bot, api_client=api_client)

    if action == "delete":
        success = await svc.delete_message(chat_id=chat_id, message_id=message_id)
        if success:
            await callback.answer("🗑 Xabar o'chirildi.")
            try:
                await callback.message.edit_text(
                    callback.message.text + "\n\n✅ <i>Moderator: xabar o'chirildi.</i>"
                )
            except Exception:
                pass
        else:
            await callback.answer("❌ Xabarni o'chirib bo'lmadi.")

    elif action == "fp":
        await callback.answer("✅ Soxta pozitiv belgilandi.")
        try:
            await callback.message.edit_text(
                callback.message.text + "\n\n✅ <i>Moderator: soxta pozitiv.</i>"
            )
        except Exception:
            pass

    elif action == "warn":
        await svc.warn_user(
            chat_id=chat_id,
            user_id=user_id,
            message_id=message_id,
            message_text="",
            reason="Moderator qarori",
        )
        await callback.answer("⚠️ Ogohlantirish yuborildi.")

    elif action == "mute":
        success = await svc.mute_user(
            chat_id=chat_id,
            user_id=user_id,
            duration_seconds=_BAN_MUTE_DURATION,
            message_id=message_id,
            reason="Moderator qarori",
        )
        if success:
            await callback.answer("🔇 Foydalanuvchi jim qilindi.")
            try:
                await callback.message.edit_reply_markup(reply_markup=None)
            except Exception:
                pass
        else:
            await callback.answer("❌ Jim qilib bo'lmadi.")

    elif action == "ban":
        success = await svc.permanent_ban_user(
            chat_id=chat_id,
            user_id=user_id,
            message_id=message_id,
            reason="Moderator qarori",
        )
        if success:
            await callback.answer("🚫 Foydalanuvchi bloklandi.")
            try:
                await callback.message.edit_reply_markup(reply_markup=None)
            except Exception:
                pass
        else:
            await callback.answer("❌ Bloklash muvaffaqiyatsiz.")

    elif action == "whitelist":
        await callback.answer("✅ Foydalanuvchi oq ro'yxatga qo'shildi.")
        try:
            await callback.message.edit_text(
                callback.message.text + "\n\n✅ <i>Moderator: oq ro'yxatga qo'shildi.</i>"
            )
        except Exception:
            pass

    elif action == "cancel":
        await callback.answer("❌ Bekor qilindi.")
        try:
            await callback.message.edit_reply_markup(reply_markup=None)
        except Exception:
            pass

    else:
        await callback.answer("❌ Noma'lum buyruq.")


@router.callback_query(F.data.startswith("settings:"))
async def handle_settings_callback(callback: CallbackQuery, **data: Any) -> None:
    if callback.data is None:
        await callback.answer()
        return

    parts = callback.data.split(":")
    action = parts[1] if len(parts) > 1 else ""

    if action == "close":
        await callback.answer()
        try:
            await callback.message.delete()  # type: ignore[union-attr]
        except Exception:
            pass
        return

    if action == "language":
        from keyboards.inline.settings import language_keyboard
        await callback.answer()
        try:
            await callback.message.edit_text(  # type: ignore[union-attr]
                "🌐 <b>Til tanlang:</b>",
                reply_markup=language_keyboard(),
            )
        except Exception:
            pass

    elif action == "lang" and len(parts) > 2:
        lang = parts[2]
        api_client: FindSpamAPIClient = data["api_client"]
        from redis.asyncio import Redis
        from services.group_service import GroupService
        redis: Redis = data["redis"]
        svc = GroupService(redis=redis, api_client=api_client)
        if callback.message:
            await svc.update_settings(callback.message.chat.id, {"language": lang})
        await callback.answer(f"✅ Til o'zgartirildi: {lang}")

    elif action == "view":
        await callback.answer("📋 Joriy sozlamalar.")

    elif action == "back":
        from keyboards.inline.settings import settings_menu_keyboard
        await callback.answer()
        try:
            await callback.message.edit_text(  # type: ignore[union-attr]
                "⚙️ <b>Guruh sozlamalari</b>\n\nQuyidagi bo'limlardan birini tanlang:",
                reply_markup=settings_menu_keyboard(),
            )
        except Exception:
            pass

    else:
        await callback.answer("🔧 Tez orada qo'shiladi.")
