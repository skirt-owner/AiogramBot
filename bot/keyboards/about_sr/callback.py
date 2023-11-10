from aiogram.filters.callback_data import CallbackData


class AboutSrCallback(CallbackData, prefix="about_sr_menu"):
    option: int
