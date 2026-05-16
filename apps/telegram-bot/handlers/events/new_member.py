from aiogram import Router
from aiogram.types import ChatMemberUpdated

router = Router()


@router.chat_member()
async def handle_new_member(event: ChatMemberUpdated) -> None:
    pass
