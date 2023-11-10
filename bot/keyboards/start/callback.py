from aiogram.filters.callback_data import CallbackData


class StartCallback(CallbackData, prefix="start_menu"):
    option: int
