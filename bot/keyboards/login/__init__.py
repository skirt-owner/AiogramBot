__all__ = ["login_types_keyboard", "login_time_keyboard"]

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.cancel import cancel_button
from .callback import LoginTimeCallback, LoginMenuCallback

login_types_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="По номеру договора",
                callback_data=LoginMenuCallback(option=1).pack()
            ),
        ],

        [
            InlineKeyboardButton(
                text="По коду из СМС",
                callback_data=LoginMenuCallback(option=2).pack()
            ),
        ],

        [cancel_button],
    ]
)

login_time_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="1 день",
                callback_data=LoginTimeCallback(time=1).pack()
            ),
            InlineKeyboardButton(
                text="5 дней",
                callback_data=LoginTimeCallback(time=5).pack()
            ),
        ],

        [
            InlineKeyboardButton(
                text="10 дней",
                callback_data=LoginTimeCallback(time=10).pack()
            ),
            InlineKeyboardButton(
                text="30 дней",
                callback_data=LoginTimeCallback(time=30).pack()
            ),
        ],

        [
            InlineKeyboardButton(
                text="90 дней",
                callback_data=LoginTimeCallback(time=90).pack()
            )
        ],

        [cancel_button],
    ]
)