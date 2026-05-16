from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("stats"))
async def cmd_stats(message: Message) -> None:
    pass
