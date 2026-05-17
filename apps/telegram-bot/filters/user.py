from __future__ import annotations

from aiogram.filters import Filter
from aiogram.types import Message


class NotBot(Filter):
    """Passes when the message sender is a real user (not a bot)."""

    async def __call__(self, message: Message) -> bool:
        return message.from_user is not None and not message.from_user.is_bot


class IsNotMuted(Filter):
    """Passes when the user is not currently muted (injected via middleware)."""

    async def __call__(self, message: Message, is_muted: bool = False) -> bool:
        return not is_muted
