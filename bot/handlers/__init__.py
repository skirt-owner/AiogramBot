__all__ = ["setup"]

from aiogram import F, Router
from aiogram import Dispatcher
from aiogram.filters import CommandStart, Command

from bot.filters.isloggedin import IsLoggedIn
from bot.handlers.help import help_command
from bot.handlers import login, cancel, about_sr, my_home, store
from bot.handlers.start import logged_in_start, not_logged_in_start

# Callbacks
from bot.keyboards.about_sr.callback import AboutSrCallback
from bot.keyboards.login.callback import LoginTimeCallback, LoginMenuCallback
from bot.keyboards.start.callback import StartCallback
from bot.keyboards.store.callback import StoreCallback

main_router = Router()


def register_message_handlers() -> None:
    """
    Регистрация хэндлеров
    :return:
    """

    main_router.message.register(
        logged_in_start,
        IsLoggedIn(),
        CommandStart()
    )

    main_router.message.register(
        not_logged_in_start,
        ~IsLoggedIn(),
        CommandStart()
    )

    main_router.message.register(
        help_command,
        Command("help")
    )

    cancel.router.message.register(
        cancel.cancel_command_logged_in,
        IsLoggedIn(),
        Command("cancel")
    )

    cancel.router.message.register(
        cancel.cancel_command_not_logged_in,
        ~IsLoggedIn(),
        Command("cancel")
    )

    cancel.router.callback_query.register(
        cancel.cancel_callback_logged_in,
        IsLoggedIn(),
        F.data == "cancel"
    )

    cancel.router.callback_query.register(
        cancel.cancel_callback_not_logged_in,
        ~IsLoggedIn(),
        F.data == "cancel"
    )

    login.router.callback_query.register(
        login.login,
        ~IsLoggedIn(),
        StartCallback.filter(F.option == 1)
    )

    login.router.callback_query.register(
        login.login_by_sms,
        ~IsLoggedIn(),
        LoginMenuCallback.filter(F.option == 2)
    )

    login.router.message.register(
        login.get_sms_code,
        ~IsLoggedIn(),
        login.LoginBySMS.waiting_for_sms_code
    )

    login.router.callback_query.register(
        login.login_by_contract_number,
        ~IsLoggedIn(),
        LoginMenuCallback.filter(F.option == 1)
    )

    login.router.message.register(
        login.get_contract_number,
        ~IsLoggedIn(),
        login.LoginByContract.waiting_for_contract_number
    )

    login.router.message.register(
        login.get_code_word,
        ~IsLoggedIn(),
        login.LoginByContract.waiting_for_code_word
    )

    login.router.callback_query.register(
        login.set_login_time,
        IsLoggedIn(),
        LoginTimeCallback.filter(F.time.in_([1, 5, 10, 30, 90]))
    )

    about_sr.router.callback_query.register(
        about_sr.about_sr_logged_in,
        IsLoggedIn(),
        StartCallback.filter(F.option == 2)
    )

    about_sr.router.callback_query.register(
        about_sr.about_sr_not_logged_in,
        ~IsLoggedIn(),
        StartCallback.filter(F.option == 2)
    )

    my_home.router.callback_query.register(
        my_home.my_home,
        IsLoggedIn(),
        StartCallback.filter(F.option == 1)
    )

    store.router.callback_query.register(
        store.logged_in,
        IsLoggedIn(),
        AboutSrCallback.filter(F.option == 7)
    )

    store.router.callback_query.register(
        store.not_logged_in,
        ~IsLoggedIn(),
        AboutSrCallback.filter(F.option == 6)
    )

    store.router.callback_query.register(
        store.slider,
        StoreCallback.filter()
    )


def setup(dispatcher: Dispatcher) -> None:
    """

    :param dispatcher:
    :return:
    """
    register_message_handlers()

    main_router.include_routers(
        login.router, about_sr.router,
        my_home.router, store.router
    )

    dispatcher.include_routers(
        main_router,
        cancel.router,
    )
