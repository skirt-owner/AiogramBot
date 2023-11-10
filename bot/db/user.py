from datetime import datetime

from redis.asyncio.client import Redis
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.db.models import User


async def get_last_update_date(
        user_id: int,
        async_session_maker: async_sessionmaker
) -> datetime:
    """

    :param user_id:
    :param async_session_maker:
    :return:
    """
    async with async_session_maker() as session:
        async with session.begin():
            sql_result = await session.execute(select(User.update_date).where(User.user_id == user_id))
            return sql_result.scalars().first()


async def get_login_time(
        user_id: int,
        async_session_maker: async_sessionmaker
) -> int:
    """

    :param user_id:
    :param async_session_maker:
    :return:
    """
    async with async_session_maker() as session:
        async with session.begin():
            sql_result = await session.execute(select(User.login_time).where(User.user_id == user_id))
            return sql_result.scalars().first()


async def update_login_time(
        user_id: int,
        async_session_maker: async_sessionmaker,
        new_data=-1
) -> None:
    """

    :param new_data:
    :param user_id:
    :param async_session_maker:
    :return:
    """
    async with async_session_maker() as session:
        async with session.begin():
            await session.execute(
                update(User).values({"login_time": new_data}).where(User.user_id == user_id)
            )


async def update_login_attempts(
        user_id: int,
        async_session_maker: async_sessionmaker,
        new_data=None
) -> None:
    """

    :param new_data:
    :param user_id:
    :param async_session_maker:
    :return:
    """
    if new_data is None:
        new_data = (await get_login_attempts(
            user_id=user_id,
            async_session_maker=async_session_maker
        )) + 1
    async with async_session_maker() as session:
        async with session.begin():
            await session.execute(
                update(User).values({"login_attempts": new_data}).where(User.user_id == user_id)
            )


async def get_login_attempts(
        user_id: int,
        async_session_maker: async_sessionmaker
) -> int:
    """

    :param user_id:
    :param async_session_maker:
    :return:
    """
    async with async_session_maker() as session:
        async with session.begin():
            sql_result = await session.execute(select(User.login_attempts).where(User.user_id == user_id))
            return sql_result.scalars().first()


async def update_login(
        user_id: int,
        async_session_maker: async_sessionmaker,
        redis: Redis,
        new_data: bool
) -> None:
    """

    :param redis:
    :param new_data:
    :param user_id:
    :param async_session_maker:
    :return:
    """
    name = f"user_logged_in:{user_id}"
    expire_time = 600
    await redis.set(name=name, value=int(new_data))
    await redis.expire(name=name, time=expire_time)

    async with async_session_maker() as session:
        async with session.begin():
            await session.execute(
                update(User).values({"login": new_data}).where(User.user_id == user_id)
            )


async def is_user_logged_in(
        user_id: int,
        async_session_maker: async_sessionmaker,
        redis: Redis
) -> bool:
    """
    Проверка на User(Base).login
    :param redis:
    :param user_id:
    :param async_session_maker:
    :return:
    """
    name = f"user_logged_in:{user_id}"
    redis_result = await redis.get(name=name)

    if redis_result is None:
        async with async_session_maker() as session:
            async with session.begin():
                sql_result = await session.execute(select(User.login).where(User.user_id == user_id))
                is_logged_in = sql_result.scalars().first()

                expire_time = 600
                await redis.set(name=name, value=int(is_logged_in))
                await redis.expire(name=name, time=expire_time)

                return is_logged_in
    else:
        return bool(int(redis_result))


async def get_user(
        user_id: int,
        async_session_maker: async_sessionmaker) -> User:
    """
    Получить пользователя по его id
    :param user_id:
    :param async_session_maker:
    :return:
    """
    async with async_session_maker() as session:
        async with session.begin():
            sql_result = await session.execute(select(User).where(User.user_id == user_id))
            return sql_result.scalars().first()


async def create_user(
        user_id: int,
        async_session_maker: async_sessionmaker,
        redis: Redis) -> None:
    """
    Создание записи о пользователе
    :param redis:
    :param user_id:
    :param async_session_maker:
    :return:
    """
    async with async_session_maker() as session:
        async with session.begin():
            user = User(
                user_id=user_id,
                login_attempts=0,
                login=False,
                login_time=-1
            )
            session.add(user)

    expire_time = 600
    name = f"user_exists:{user_id}"
    await redis.set(name=name, value=1)
    await redis.expire(name=name, time=expire_time)


async def is_user_exists(
        user_id: int,
        async_session_maker: async_sessionmaker,
        redis: Redis) -> bool:
    """
    Проверка на существование пользователя в БД или в Redis
    :param user_id:
    :param async_session_maker:
    :param redis:
    :return:
    """
    name = f"user_exists:{user_id}"
    redis_result = await redis.get(name=name)

    if redis_result is None:
        async with async_session_maker() as session:
            async with session.begin():
                sql_result = await session.execute(select(User).where(User.user_id == user_id))
                sql_result = sql_result.first() is not None

                expire_time = 600
                await redis.set(name=name, value=int(sql_result))
                await redis.expire(name=name, time=expire_time)

                return bool(sql_result)
    else:
        return bool(int(redis_result))
