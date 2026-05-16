from aiogram import Router
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query()
async def handle_moderation_callback(callback: CallbackQuery) -> None:
    pass
