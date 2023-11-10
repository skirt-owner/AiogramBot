from typing import Union

from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.db.user import is_user_logged_in


class IsLoggedIn(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(
            self,
            event: Union[Message, CallbackQuery],
            async_session_maker: async_sessionmaker,
            redis: Redis
    ) -> bool:
        user = event.from_user

        user_logged_in = await is_user_logged_in(
            user_id=user.id,
            async_session_maker=async_session_maker,
            redis=redis
        )

        return user_logged_in
