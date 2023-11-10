from aiogram import Router, types

from bot import keyboards
from bot.keyboards.start.callback import StartCallback

router = Router()


async def my_home(query: types.CallbackQuery, callback_data: StartCallback) -> None:
    """

    :param query:
    :param callback_data:
    :return:
    """
    await query.message.delete()

    await query.message.answer(
        text="Подробнее о SR",
        reply_markup=keyboards.my_home.my_home_keyboard
    )
    await query.answer(show_alert=False)