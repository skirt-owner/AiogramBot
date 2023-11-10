__all__ = ["logged_in", "not_logged_in"]

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards import cancel_button
from .callback import AboutSrCallback

logged_in = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Обратная связь",
                callback_data=AboutSrCallback(option=1).pack()
            ),
            InlineKeyboardButton(
                text="Возможности SR",
                callback_data=AboutSrCallback(option=2).pack()
            ),
        ],

        [
            InlineKeyboardButton(
                text="Мы в соц. сетях",
                callback_data=AboutSrCallback(option=3).pack()
            ),
            InlineKeyboardButton(
                text="Сообщить о проблеме",
                callback_data=AboutSrCallback(option=4).pack()
            ),
        ],

        [
            InlineKeyboardButton(
                text="Цены",
                callback_data=AboutSrCallback(option=5).pack()
            ),
            InlineKeyboardButton(
                text="Добавить новые возможности",
                callback_data=AboutSrCallback(option=6).pack()
            ),
        ],

        [
            InlineKeyboardButton(
                text="STORE",
                callback_data=AboutSrCallback(option=7).pack()
            ),
        ],

        [cancel_button],
    ]
)

not_logged_in = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Обратная связь",
                callback_data=AboutSrCallback(option=1).pack()
            ),
            InlineKeyboardButton(
                text="Возможности SR",
                callback_data=AboutSrCallback(option=2).pack()
            ),
        ],

        [
            InlineKeyboardButton(
                text="Мы в соц. сетях",
                callback_data=AboutSrCallback(option=3).pack()
            ),
            InlineKeyboardButton(
                text="Цены",
                callback_data=AboutSrCallback(option=4).pack()
            ),
        ],

        [
            InlineKeyboardButton(
                text="Заказать установку",
                callback_data=AboutSrCallback(option=5).pack()
            ),
            InlineKeyboardButton(
                text="STORE",
                callback_data=AboutSrCallback(option=6).pack()
            ),
        ],

        [cancel_button],
    ]
)
