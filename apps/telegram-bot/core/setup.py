from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from core.config import get_bot_settings

settings = get_bot_settings()


def build_dispatcher() -> Dispatcher:
    storage = RedisStorage(Redis.from_url(settings.redis_url))
    dp = Dispatcher(storage=storage)

    _register_middlewares(dp)
    _register_handlers(dp)

    return dp


def _register_middlewares(dp: Dispatcher) -> None:
    from middlewares.logging import LoggingMiddleware
    from middlewares.rate_limiter import RateLimiterMiddleware
    from middlewares.spam_detector import SpamDetectorMiddleware

    dp.message.middleware(LoggingMiddleware())
    dp.message.middleware(RateLimiterMiddleware())
    dp.message.middleware(SpamDetectorMiddleware())


def _register_handlers(dp: Dispatcher) -> None:
    from handlers.commands.start import router as start_router
    from handlers.commands.settings import router as settings_router
    from handlers.commands.stats import router as stats_router
    from handlers.messages.text import router as text_router
    from handlers.callbacks.moderation import router as moderation_router
    from handlers.events.new_member import router as new_member_router

    dp.include_router(start_router)
    dp.include_router(settings_router)
    dp.include_router(stats_router)
    dp.include_router(text_router)
    dp.include_router(moderation_router)
    dp.include_router(new_member_router)
