import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.config_reader import config
from bot.handlers import commands, callbacks,location
from bot.middlewares import DbSessionMiddleware
from bot.ui_commands import set_ui_commands
from bot.config_reader import config

engine = create_async_engine(url=config.db_url, echo=True)
session_maker = async_sessionmaker(engine, expire_on_commit=False)




async def main():
    bot = Bot(config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode="HTML"))

    # Setup dispatcher and bind routers to it
    dp = Dispatcher()
    dp.update.middleware(DbSessionMiddleware(session_pool=session_maker))

    # Automatically reply to all callbacks
    dp.callback_query.middleware(CallbackAnswerMiddleware())

    # Register handlers
    dp.include_router(commands.router)
    dp.include_router(callbacks.router)
    dp.include_router(location.router)

    # Set bot commands in UI
    await set_ui_commands(bot)

    # Run bot
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
