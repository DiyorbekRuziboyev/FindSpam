from __future__ import annotations

import asyncio
import logging

import structlog
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from redis.asyncio import Redis

from core.api_client import FindSpamAPIClient
from core.config import get_bot_settings
from core.setup import build_dispatcher

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logger = logging.getLogger(__name__)
settings = get_bot_settings()


async def main() -> None:
    bot = Bot(
        token=settings.telegram_bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    redis = Redis.from_url(settings.redis_url, decode_responses=True)
    api_client = FindSpamAPIClient()

    dp: Dispatcher = build_dispatcher(redis=redis, settings=settings)
    dp["api_client"] = api_client

    logger.info("FindSpam Telegram Bot starting up")

    try:
        if settings.use_webhook:
            from aiohttp import web
            from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

            app = web.Application()
            handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
            handler.register(app, path=settings.webhook_path)
            setup_application(app, dp, bot=bot)

            await bot.set_webhook(
                url=settings.webhook_url,
                secret_token=settings.webhook_secret or None,
            )
            web.run_app(app, host="0.0.0.0", port=settings.webhook_port)
        else:
            await bot.delete_webhook(drop_pending_updates=True)
            await dp.start_polling(
                bot,
                allowed_updates=dp.resolve_used_update_types(),
            )
    finally:
        logger.info("FindSpam Telegram Bot shutting down")
        await api_client.aclose()
        await redis.aclose()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
