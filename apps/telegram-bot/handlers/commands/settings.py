from __future__ import annotations

from typing import Any

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from filters.admin import IsAdmin
from filters.chat import IsGroupMessage
from keyboards.inline.settings import settings_menu_keyboard

router = Router()


@router.message(Command("settings"), IsGroupMessage(), IsAdmin())
async def cmd_settings(message: Message, **data: Any) -> None:
    text = (
        "⚙️ <b>Guruh sozlamalari</b>\n\n"
        "Quyidagi bo'limlardan birini tanlang:"
    )
    await message.answer(text, reply_markup=settings_menu_keyboard())
