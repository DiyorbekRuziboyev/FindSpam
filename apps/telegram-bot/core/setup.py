from __future__ import annotations

from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from core.config import BotSettings, get_bot_settings


def build_dispatcher(redis: Redis, settings: BotSettings | None = None) -> Dispatcher:
    """Build and configure the aiogram Dispatcher with DI via workflow_data.

    All shared resources (redis, api_client) are stored in dp["key"] so that
    middlewares and handlers receive them via data["key"] without module singletons.
    """
    if settings is None:
        settings = get_bot_settings()

    storage = RedisStorage(redis)
    dp = Dispatcher(storage=storage)

    dp["redis"] = redis
    dp["settings"] = settings

    _register_middlewares(dp, settings)
    _register_handlers(dp)

    return dp


def _register_middlewares(dp: Dispatcher, settings: BotSettings) -> None:
    from middlewares.logging import LoggingMiddleware
    from middlewares.rate_limiter import RateLimiterMiddleware
    from middlewares.spam_detector import SpamDetectorMiddleware

    dp.message.outer_middleware(LoggingMiddleware())
    dp.message.outer_middleware(
        RateLimiterMiddleware(
            limit=settings.rate_limit_messages,
            window=settings.rate_limit_window,
        )
    )
    dp.message.middleware(SpamDetectorMiddleware())


def _register_handlers(dp: Dispatcher) -> None:
    from handlers.callbacks.moderation import router as moderation_cb_router
    from handlers.commands.moderation import router as moderation_cmd_router
    from handlers.commands.settings import router as settings_router
    from handlers.commands.start import router as start_router
    from handlers.commands.stats import router as stats_router
    from handlers.events.new_member import router as new_member_router
    from handlers.messages.text import router as text_router

    dp.include_router(start_router)
    dp.include_router(moderation_cmd_router)
    dp.include_router(settings_router)
    dp.include_router(stats_router)
    dp.include_router(text_router)
    dp.include_router(moderation_cb_router)
    dp.include_router(new_member_router)
