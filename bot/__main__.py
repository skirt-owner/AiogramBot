import io
import logging
import asyncio
import pathlib

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import WebAppInfo, MenuButtonWebApp, InlineKeyboardMarkup, InlineKeyboardButton, InputFile, \
    BufferedInputFile, FSInputFile
from redis.asyncio.client import Redis

from bot import config, handlers
from bot.commands import generate_bot_commands
from bot.db.base import Base
from bot.db.engine import create_database_url, \
    create_async_engine, \
    init_models, \
    get_async_session_maker
from bot.middlewares.blockuser import BlockUser
from bot.middlewares.checkevent import CheckEvent
from bot.middlewares.checkuser import CheckUser


def setup_env() -> None:
    """
    Настройка переменных окружения
    :return:
    """
    from dotenv import load_dotenv
    path = pathlib.Path(__file__).parent.parent
    dotenv_path = path.joinpath('.venv')
    if dotenv_path.exists():
        load_dotenv(dotenv_path)


async def main() -> None:
    """
    Главная точка входа
    :return:
    """
    # TODO настроить создание Redis
    redis = Redis(decode_responses=True)
    dispatcher = Dispatcher(storage=RedisStorage(redis=redis))

    handlers.setup(dispatcher)

    dispatcher.message.outer_middleware(CheckUser())
    dispatcher.callback_query.outer_middleware(CheckUser())

    dispatcher.message.middleware(BlockUser())
    dispatcher.callback_query.middleware(BlockUser())

    dispatcher.callback_query.outer_middleware(CheckEvent())

    bot = Bot(token=config.telegram_token.get_secret_value())
    await bot.set_my_commands(generate_bot_commands())

    database_url = create_database_url()
    async_engine = create_async_engine(database_url)
    await init_models(async_engine, Base.metadata)
    async_session_maker = get_async_session_maker(async_engine)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dispatcher.start_polling(
            bot,
            allowed_updates=dispatcher.resolve_used_update_types(),
            close_bot_session=True,
            async_session_maker=async_session_maker,
            redis=redis
        )
    finally:
        await dispatcher.storage.close()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) > %(message)s"
    )
    setup_env()
    asyncio.run(main())
