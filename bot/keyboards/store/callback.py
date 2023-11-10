from aiogram.filters.callback_data import CallbackData


class StoreCallback(CallbackData, prefix="store_menu"):
    page: int

