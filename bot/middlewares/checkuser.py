from typing import Any, Dict, Callable, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from bot.db.user import is_user_exists, create_user


class CheckUser(BaseMiddleware):
    def __init__(self) -> None:
        pass

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:

        async_session_maker = data['async_session_maker']
        redis = data['redis']

        user = event.from_user

        if not await is_user_exists(
                user_id=user.id,
                async_session_maker=async_session_maker,
                redis=redis
        ):
            await create_user(
                user_id=user.id,
                async_session_maker=async_session_maker,
                redis=redis
            )

        return await handler(event, data)
