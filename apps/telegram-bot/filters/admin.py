from __future__ import annotations

from aiogram.filters import Filter
from aiogram.types import ChatMemberAdministrator, ChatMemberOwner, Message


class IsAdmin(Filter):
    """Passes when the message sender is a group administrator or owner."""

    async def __call__(self, message: Message) -> bool:
        if not message.from_user or message.chat.type == "private":
            return False
        member = await message.chat.get_member(message.from_user.id)
        return isinstance(member, (ChatMemberAdministrator, ChatMemberOwner))


class IsSuperAdmin(Filter):
    """Passes when the message sender is the group owner (creator)."""

    async def __call__(self, message: Message) -> bool:
        if not message.from_user or message.chat.type == "private":
            return False
        member = await message.chat.get_member(message.from_user.id)
        return isinstance(member, ChatMemberOwner)
