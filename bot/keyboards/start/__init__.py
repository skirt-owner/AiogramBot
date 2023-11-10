__all__ = ["logged_in", "not_logged_in"]

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .callback import StartCallback


logged_in = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Мой дом",
                callback_data=StartCallback(option=1).pack()
            ),
        ],

        [
            InlineKeyboardButton(
                text="Подробнее о SR",
                callback_data=StartCallback(option=2).pack()
            ),
        ],
    ]
)

not_logged_in = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Авторизация",
                callback_data=StartCallback(option=1).pack()
            ),
        ],

        [
            InlineKeyboardButton(
                text="Подробнее о SR",
                callback_data=StartCallback(option=2).pack()
            ),
        ],
    ]
)