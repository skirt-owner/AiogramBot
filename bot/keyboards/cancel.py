from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

cancel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Отмена", callback_data="cancel"),
        ],
    ]
)

cancel_button = InlineKeyboardButton(text="Отмена", callback_data="cancel")