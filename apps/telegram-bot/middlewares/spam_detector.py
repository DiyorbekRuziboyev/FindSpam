from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message

from core.api_client import api_client


class SpamDetectorMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        if not event.text and not event.caption:
            return await handler(event, data)

        text = event.text or event.caption or ""
        metadata = {
            "user_id": event.from_user.id if event.from_user else None,
            "chat_id": event.chat.id,
            "message_id": event.message_id,
        }

        prediction = await api_client.analyze_message(text, metadata)
        data["spam_prediction"] = prediction

        return await handler(event, data)
