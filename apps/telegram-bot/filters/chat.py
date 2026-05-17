from __future__ import annotations

from aiogram.filters import Filter
from aiogram.types import Message


class IsGroupMessage(Filter):
    """Passes for messages sent in groups or supergroups (not private/channel)."""

    async def __call__(self, message: Message) -> bool:
        return message.chat.type in ("group", "supergroup")
