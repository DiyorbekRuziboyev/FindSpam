from typing import Any

from aiogram import F, Router
from aiogram.types import Message

router = Router()


@router.message(F.text)
async def handle_text_message(message: Message, spam_prediction: dict[str, Any]) -> None:
    pass
