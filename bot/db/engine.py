from sqlalchemy import URL, MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine

from bot import config


def get_async_session_maker(engine: AsyncEngine) -> async_sessionmaker:
    """
    Получение создателя сессии для SQL запросов
    :param engine:
    :return:
    """
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )


def create_database_url() -> URL:
    """
    Создание ссылки для доступа к БД
    :return:
    """
    return URL.create(
        drivername="postgresql+asyncpg",
        username=config.postgres_username,
        password=config.postgres_password.get_secret_value(),
        host=config.postgres_host.get_secret_value(),
        port=config.postgres_port,
        database=config.postgres_database
    )


def create_async_engine(database_url: URL) -> AsyncEngine:
    """
    Создание асинхронного engine
    :param database_url:
    :return:
    """
    return _create_async_engine(
        database_url,
        echo=True
    )


async def init_models(engine: AsyncEngine, metadata: MetaData) -> None:
    # TODO заменить на Alembic
    """
    Создание таблиц
    :param engine:
    :param metadata:
    :return:
    """
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)