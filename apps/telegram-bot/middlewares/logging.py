from __future__ import annotations

import time
from typing import Any, Awaitable, Callable

import structlog
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

logger = structlog.get_logger(__name__)


class LoggingMiddleware(BaseMiddleware):
    """Outer middleware: structured JSON logging for all processed messages."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        start = time.monotonic()
        result = await handler(event, data)
        elapsed_ms = round((time.monotonic() - start) * 1000, 2)

        if isinstance(event, Message):
            logger.info(
                "message_processed",
                chat_id=event.chat.id,
                chat_type=event.chat.type,
                user_id=event.from_user.id if event.from_user else None,
                message_id=event.message_id,
                content_type=str(event.content_type),
                elapsed_ms=elapsed_ms,
            )
        return result
