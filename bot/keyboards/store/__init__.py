__all__ = ["generate"]

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .callback import StoreCallback
from bot.keyboards import cancel_button


def generate(page: int, data_length: int) -> InlineKeyboardMarkup:
    """

    :param page:
    :param data_length:
    :return:
    """
    row = []

    if page > data_length:
        page = data_length
    elif page < 1:
        page = 1

    if page == 1:
        row.append(InlineKeyboardButton(
            text="<-",
            callback_data=StoreCallback(page=-1).pack()
        ))
        row.append(InlineKeyboardButton(
            text="<<-",
            callback_data=StoreCallback(page=-1).pack()
        ))
    else:
        row.append(InlineKeyboardButton(
            text="<<1",
            callback_data=StoreCallback(page=1).pack()
        ))
        row.append(InlineKeyboardButton(
            text=f"<{page - 1}",
            callback_data=StoreCallback(page=page-1).pack()
        ))

    row.append(InlineKeyboardButton(
        text=f"~{page}~",
        callback_data=StoreCallback(page=-1).pack()
    ))

    if data_length == page:
        row.append(InlineKeyboardButton(
            text="->",
            callback_data=StoreCallback(page=-1).pack()
        ))
        row.append(InlineKeyboardButton(
            text="->>",
            callback_data=StoreCallback(page=-1).pack()
        ))
    else:
        row.append(InlineKeyboardButton(
            text=f"{page+1}>",
            callback_data=StoreCallback(page=page+1).pack()
        ))
        row.append(InlineKeyboardButton(
            text=f"{data_length}>>",
            callback_data=StoreCallback(page=data_length).pack()
        ))

    return InlineKeyboardMarkup(
        inline_keyboard=[
            row,
            []
            [cancel_button]
        ]
    )
