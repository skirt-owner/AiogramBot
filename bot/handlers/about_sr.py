from aiogram import types, Router

from bot import keyboards
from bot.keyboards.start.callback import StartCallback

router = Router()


async def about_sr_logged_in(query: types.CallbackQuery, callback_data: StartCallback) -> None:
    """

    :param query:
    :param callback_data:
    :return:
    """
    await query.message.delete()

    await query.message.answer(
        text="Подробнее о SR",
        reply_markup=keyboards.about_sr.logged_in
    )
    await query.answer(show_alert=False)


async def about_sr_not_logged_in(query: types.CallbackQuery, callback_data: StartCallback) -> None:
    """

    :param query:
    :param callback_data:
    :return:
    """
    await query.message.delete()

    await query.message.answer(
        text="Подробнее о SR",
        reply_markup=keyboards.about_sr.not_logged_in
    )
    await query.answer(show_alert=False)