from datetime import datetime, timezone
from typing import Any, Dict, Callable, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from bot.db.user import is_user_logged_in, get_last_update_date, get_login_attempts, get_login_time, update_login, \
    update_login_time
from bot.keyboards import cancel_keyboard


# TODO добавить кэширование
class BlockUser(BaseMiddleware):
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

        user_id = event.from_user.id

        last_update_date = await get_last_update_date(
            user_id=user_id,
            async_session_maker=async_session_maker
        )

        if last_update_date is None:
            return await handler(event, data)

        is_logged_in = await is_user_logged_in(
            user_id=user_id,
            async_session_maker=async_session_maker,
            redis=redis
        )

        if is_logged_in:
            login_time = await get_login_time(
                user_id=user_id,
                async_session_maker=async_session_maker
            )
            if login_time < 0:
                return await handler(event, data)
            if (datetime.now(tz=timezone.utc) - last_update_date).total_seconds() / 86400 \
                    > login_time:
                await update_login_time(
                    user_id=user_id,
                    async_session_maker=async_session_maker
                )
                await update_login(
                    user_id=user_id,
                    async_session_maker=async_session_maker,
                    redis=redis,
                    new_data=False
                )
                await data['bot'].send_message(
                    chat_id=user_id,
                    text="Время входа в систему закончилось!",
                    reply_markup=cancel_keyboard
                )
                return
            return await handler(event, data)
        else:
            login_attempts = await get_login_attempts(
                user_id=user_id,
                async_session_maker=async_session_maker
            )

            if login_attempts == 3:
                if (datetime.now() - last_update_date).total_seconds()/60 > 3:
                    return await handler(event, data)
                else:
                    await data['bot'].send_message(
                        chat_id=user_id,
                        text="Ты заблокирован на 3 минуты!"
                    )
                    return
            if login_attempts == 6:
                if (datetime.now() - last_update_date).total_seconds() / 60 > 10:
                    return await handler(event, data)
                else:
                    await data['bot'].send_message(
                        chat_id=user_id,
                        text="Ты заблокирован на 10 минут!"
                    )
                    return
            if login_attempts > 6:
                await data['bot'].send_message(
                    chat_id=user_id,
                    text="Ты заблокирован навсегда (свяжись с @admin)!"
                )
                return
        return await handler(event, data)
