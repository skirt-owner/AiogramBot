from aiogram.filters.callback_data import CallbackData


class MyHomeCallback(CallbackData, prefix="my_home_menu"):
    option: int
