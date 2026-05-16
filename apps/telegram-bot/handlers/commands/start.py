from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    pass


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    pass
