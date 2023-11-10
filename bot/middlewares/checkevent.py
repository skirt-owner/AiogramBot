from datetime import datetime, timezone
from typing import Any, Dict, Callable, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery


class CheckEvent(BaseMiddleware):
    def __init__(self) -> None:
        pass

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
        date = event.message.date

        if (datetime.now(tz=timezone.utc) - date).total_seconds() / 3600 > 48:
            await event.answer(text="Истекло время запроса!")
            return

        return await handler(event, data)
