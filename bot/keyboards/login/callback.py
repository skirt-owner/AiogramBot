from aiogram.filters.callback_data import CallbackData


class LoginTimeCallback(CallbackData, prefix="login_time"):
    time: int


class LoginMenuCallback(CallbackData, prefix="login_menu"):
    option: int
