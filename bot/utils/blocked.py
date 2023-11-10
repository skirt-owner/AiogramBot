import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.db.user import get_login_attempts, get_login_time

block_time = {3: 3, 6: 10}


def logged_in(
        user_id: int,
        async_session_maker: async_sessionmaker
) -> int:
    """

    :param user_id:
    :param async_session_maker:
    :return:
    """
    login_time = asyncio.run(
        get_login_time(
            user_id=user_id,
            async_session_maker=async_session_maker
        )
    )

    return login_time


def not_logged_in(
        user_id: int,
        async_session_maker: async_sessionmaker
) -> int:
    """

    :param user_id:
    :param async_session_maker:
    :return:
    """
    login_attempts = asyncio.run(
        get_login_attempts(
            user_id=user_id,
            async_session_maker=async_session_maker
        )
    )

    if login_attempts in [3, 6]:
        return block_time[login_attempts]

    if login_attempts > 6:
        return 888

    return -1


