__all__ = ["my_home_keyboard"]

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards import cancel_button
from .callback import MyHomeCallback

my_home_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Постановка на охрану",
                callback_data=MyHomeCallback(option=1).pack()
            ),
        ],

        [
            InlineKeyboardButton(
                text="Безопасность",
                callback_data=MyHomeCallback(option=2).pack()
            ),
        ],

        [
            InlineKeyboardButton(
                text="Датчики",
                callback_data=MyHomeCallback(option=3).pack()
            ),
        ],

        [cancel_button],
    ]
)