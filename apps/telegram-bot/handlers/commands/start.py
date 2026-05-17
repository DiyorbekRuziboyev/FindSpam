from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    name = message.from_user.first_name if message.from_user else "User"
    if message.chat.type == "private":
        text = (
            f"👋 Salom, <b>{name}</b>!\n\n"
            "🛡 <b>FindSpamBot</b> — professional spam va scam aniqlash boti.\n\n"
            "Botni guruhga qo'shing va admin qiling — u avtomatik ravishda:\n"
            "• Spam va scam xabarlarni o'chiradi\n"
            "• Fishing havolalarini bloklaydi\n"
            "• Foydalanuvchilarni ogohlantiradi va jazolaydi\n"
            "• Haqiqiy vaqt rejimida monitoring qiladi\n\n"
            "📋 Buyruqlar ro'yxati: /help"
        )
    else:
        text = (
            "🛡 <b>FindSpamBot</b> faollashtirildi!\n\n"
            "Guruhingiz endi avtomatik moderatsiya ostida.\n"
            "Sozlamalar: /settings"
        )
    await message.answer(text)


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    text = (
        "📋 <b>FindSpamBot buyruqlari</b>\n\n"
        "<b>Moderatsiya:</b>\n"
        "/warn — foydalanuvchini ogohlantirish\n"
        "/mute — foydalanuvchini jim qilish\n"
        "/ban — foydalanuvchini bloklash\n"
        "/unban — blokdan chiqarish\n"
        "/unmute — jim qilishni bekor qilish\n"
        "/kick — guruhdan haydash\n\n"
        "<b>Statistika va sozlamalar:</b>\n"
        "/stats — guruh statistikasi\n"
        "/settings — bot sozlamalari\n\n"
        "<b>Qo'llanma:</b>\n"
        "Buyruq ishlatish uchun reply yoki username bilan: "
        "<code>/warn @username sabab</code>"
    )
    await message.answer(text)
