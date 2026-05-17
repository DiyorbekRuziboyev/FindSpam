from __future__ import annotations

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def settings_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🌐 Language", callback_data="settings:language")
    builder.button(text="🛡 Spam threshold", callback_data="settings:spam_threshold")
    builder.button(text="🌊 Flood protection", callback_data="settings:flood")
    builder.button(text="🔒 Auto-ban", callback_data="settings:auto_ban")
    builder.button(text="📋 View current", callback_data="settings:view")
    builder.button(text="❌ Close", callback_data="settings:close")
    builder.adjust(2)
    return builder.as_markup()


def language_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🇺🇿 O'zbek (Latin)", callback_data="settings:lang:uz_lat")
    builder.button(text="🇺🇿 Ўзбек (Кирил)", callback_data="settings:lang:uz_cyr")
    builder.button(text="🇷🇺 Русский", callback_data="settings:lang:ru")
    builder.button(text="🇬🇧 English", callback_data="settings:lang:en")
    builder.button(text="⬅️ Back", callback_data="settings:back")
    builder.adjust(2)
    return builder.as_markup()


def confirm_keyboard(action: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Confirm", callback_data=f"confirm:{action}")
    builder.button(text="❌ Cancel", callback_data="confirm:cancel")
    builder.adjust(2)
    return builder.as_markup()
