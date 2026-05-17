from __future__ import annotations

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def moderation_action_keyboard(message_id: int, user_id: int) -> InlineKeyboardMarkup:
    """Inline keyboard for reviewing a flagged message: confirm / false-positive / escalate."""
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🗑 Delete message",
        callback_data=f"mod:delete:{message_id}:{user_id}",
    )
    builder.button(
        text="✅ Not spam",
        callback_data=f"mod:fp:{message_id}:{user_id}",
    )
    builder.adjust(2)
    builder.button(
        text="⚠️ Warn user",
        callback_data=f"mod:warn:{message_id}:{user_id}",
    )
    builder.button(
        text="🔇 Mute 10 min",
        callback_data=f"mod:mute:{message_id}:{user_id}",
    )
    builder.button(
        text="🚫 Ban user",
        callback_data=f"mod:ban:{message_id}:{user_id}",
    )
    builder.adjust(2, 3)
    return builder.as_markup()


def whitelist_keyboard(message_id: int, user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="✅ Whitelist user",
        callback_data=f"mod:whitelist:{message_id}:{user_id}",
    )
    builder.button(
        text="❌ Cancel",
        callback_data=f"mod:cancel:{message_id}:{user_id}",
    )
    builder.adjust(2)
    return builder.as_markup()
