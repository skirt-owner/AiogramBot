from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .callback import StoreCallback
from bot.db import items


def generate(next_page: int) -> list:
    data_length = len(items)
    current_page = next_page - 1

    row = []

    if current_page == 1:
        row.append(InlineKeyboardButton(
            text="-",
            callback_data=StoreCallback(next_page=-1).pack()
        ))
        row.append(InlineKeyboardButton(
            text="-",
            callback_data=StoreCallback(next_page=-1).pack()
        ))
    else:
        row.append(InlineKeyboardButton(
            text="<<1",
            callback_data=StoreCallback(next_page=1).pack()
        ))

    if current_page > 1:
        row.append(InlineKeyboardButton(
            text=f"<{current_page - 1}",
            callback_data=StoreCallback(next_page=current_page - 1).pack()
        ))

    row.append(InlineKeyboardButton(
        text=f"~{current_page}~",
        callback_data=StoreCallback(next_page=-1).pack()
    ))

    if data_length == current_page:
        row.append(InlineKeyboardButton(
            text="-",
            callback_data=StoreCallback(next_page=-1).pack()
        ))
        row.append(InlineKeyboardButton(
            text="-",
            callback_data=StoreCallback(next_page=-1).pack()
        ))
    else:
        row.append(InlineKeyboardButton(
            text=f"{next_page}>",
            callback_data=StoreCallback(next_page=next_page).pack()
        ))
        row.append(InlineKeyboardButton(
            text=f"{data_length}>>",
            callback_data=StoreCallback(next_page=data_length).pack()
        ))

    return row


next_page = 2
print(generate(next_page))