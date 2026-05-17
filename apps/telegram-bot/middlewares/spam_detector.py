from __future__ import annotations

from typing import Any, Awaitable, Callable

import structlog
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

from core.api_client import FindSpamAPIClient

logger = structlog.get_logger(__name__)


class SpamDetectorMiddleware(BaseMiddleware):
    """Inner middleware: calls AI engine to classify message text.

    Injects 'spam_prediction' into handler data (dict | None).
    Reads the API client from workflow_data["api_client"] — never from module-level singleton.
    Fails open: if the AI call fails, injects None and continues without blocking the message.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)

        text = (event.text or event.caption or "").strip()
        if not text:
            data["spam_prediction"] = None
            return await handler(event, data)

        api_client: FindSpamAPIClient | None = data.get("api_client")
        if api_client is None:
            data["spam_prediction"] = None
            return await handler(event, data)

        metadata: dict[str, Any] = {
            "user_id": event.from_user.id if event.from_user else None,
            "chat_id": event.chat.id,
            "message_id": event.message_id,
            "chat_type": event.chat.type,
        }

        try:
            prediction = await api_client.analyze_message(text, metadata)
            data["spam_prediction"] = prediction
        except Exception:
            logger.exception(
                "spam_detection_failed",
                chat_id=event.chat.id,
                user_id=metadata["user_id"],
            )
            data["spam_prediction"] = None

        return await handler(event, data)
