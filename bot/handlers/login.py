from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.db.user import update_login, update_login_attempts, update_login_time
from bot.keyboards import login_types_keyboard, cancel_keyboard
from bot.keyboards.login import login_time_keyboard
from bot.keyboards.login.callback import LoginTimeCallback, LoginMenuCallback
from bot.keyboards.start.callback import StartCallback

right_contract = "12345"
right_code_word = "qwerty"
right_sms_code = "12345"
router = Router()


class LoginByContract(StatesGroup):
    waiting_for_contract_number = State()
    waiting_for_code_word = State()


class LoginBySMS(StatesGroup):
    waiting_for_sms_code = State()


async def login(query: types.CallbackQuery, callback_data: StartCallback) -> None:
    """

    :param query:
    :param callback_data:
    :return:
    """
    await query.message.delete()

    await query.message.answer(
        text="Вкладка авторизация",
        reply_markup=login_types_keyboard
    )
    await query.answer(show_alert=False)


async def login_by_sms(
        query: types.CallbackQuery,
        callback_data: LoginMenuCallback,
        state: FSMContext
) -> None:
    """

    :param query:
    :param callback_data:
    :param state:
    :return:
    """
    await state.set_state(
        LoginBySMS.waiting_for_sms_code
    )

    await query.message.delete()

    await query.message.answer(
        text="Введите код из смс",
        reply_markup=cancel_keyboard
    )
    await query.answer(show_alert=False)


async def get_sms_code(
        message: types.Message,
        async_session_maker: async_sessionmaker,
        redis: Redis,
        state: FSMContext
) -> None:
    """

    :param message:
    :param async_session_maker:
    :param redis:
    :param state:
    :return:
    """
    sms_code = message.text

    if sms_code == right_sms_code:
        await state.clear()

        await update_login_attempts(
            user_id=message.from_user.id,
            async_session_maker=async_session_maker,
            new_data=0
        )

        await update_login(
            user_id=message.from_user.id,
            async_session_maker=async_session_maker,
            redis=redis,
            new_data=True
        )

        await message.reply(
            text="Вы вошли в систему\nВыберите срок входа",
            reply_markup=login_time_keyboard
        )
    else:
        await message.reply(
            text="Вы ввели неверный код\nПопробуйте еще раз",
            reply_markup=cancel_keyboard
        )


async def login_by_contract_number(
        query: types.CallbackQuery,
        callback_data: LoginMenuCallback,
        state: FSMContext
) -> None:
    """

    :param query:
    :param callback_data:
    :param state:
    :return:
    """
    await state.set_state(
        LoginByContract.waiting_for_contract_number
    )

    await query.message.delete()

    await query.message.answer(
        text="Введите номер договора",
        reply_markup=cancel_keyboard
    )
    await query.answer(show_alert=False)


async def get_contract_number(
        message: types.Message,
        state: FSMContext
) -> None:
    """

    :param message:
    :param state:
    :return:
    """
    contract_number = message.text
    await state.update_data(contract_number=contract_number)

    await state.set_state(
        LoginByContract.waiting_for_code_word
    )

    await message.reply(
        text="Вы ввели номер договора\nВведите кодовое слово",
        reply_markup=cancel_keyboard
    )


async def get_code_word(message: types.Message,
                        async_session_maker: async_sessionmaker,
                        redis: Redis,
                        state: FSMContext) -> None:
    """

    :param redis:
    :param async_session_maker:
    :param message:
    :param state:
    :return:
    """
    data = await state.get_data()
    if data["contract_number"] == right_contract:
        code_word = message.text

        if code_word == right_code_word:
            await state.clear()

            await update_login_attempts(
                user_id=message.from_user.id,
                async_session_maker=async_session_maker,
                new_data=0
            )

            await update_login(
                user_id=message.from_user.id,
                async_session_maker=async_session_maker,
                redis=redis,
                new_data=True
            )

            await message.reply(
                text="Вы вошли в систему\nВыберите срок входа",
                reply_markup=login_time_keyboard
            )
        else:
            await update_login_attempts(
                user_id=message.from_user.id,
                async_session_maker=async_session_maker
            )

            await message.reply(
                text="Вы ввели неверное кодовое слово\nПопробуйте еще раз",
                reply_markup=cancel_keyboard
            )
    else:
        await message.reply(
            text="Ошибка входа в систему",
            reply_markup=cancel_keyboard
        )


async def set_login_time(
        query: types.CallbackQuery,
        callback_data: LoginTimeCallback,
        async_session_maker: async_sessionmaker
) -> None:
    """

    :param async_session_maker:
    :param query:
    :param callback_data:
    :return:
    """
    time = callback_data.time

    await update_login_time(
        user_id=query.from_user.id,
        async_session_maker=async_session_maker,
        new_data=time
    )

    await query.message.delete()

    await query.message.answer(
        text=f"Вы вошли в систему на {time} день/дней",
        reply_markup=cancel_keyboard
    )

    await query.answer(
        text=f"Вы выбрали период - {time}"
    )
