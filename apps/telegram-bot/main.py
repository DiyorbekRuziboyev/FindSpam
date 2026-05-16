import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from core.config import get_bot_settings
from core.setup import build_dispatcher

settings = get_bot_settings()


async def main() -> None:
    bot = Bot(
        token=settings.telegram_bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp: Dispatcher = build_dispatcher()

    if settings.use_webhook:
        from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
        from aiohttp import web

        app = web.Application()
        handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
        handler.register(app, path=settings.webhook_path)
        setup_application(app, dp, bot=bot)

        await bot.set_webhook(
            url=settings.webhook_url,
            secret_token=settings.webhook_secret,
        )
        web.run_app(app, host="0.0.0.0", port=settings.webhook_port)
    else:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
