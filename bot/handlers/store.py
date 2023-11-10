from aiogram import types, Router
from aiogram.types.input_file import FSInputFile, BufferedInputFile

from bot.keyboards.about_sr.callback import AboutSrCallback

from bot import templates, keyboards
from bot.keyboards.store.callback import StoreCallback

router = Router()

items = [
    {
        "name": "green tree",
        "price": 100,
        "currency": "rub",
        "picture": "bot/handlers/tree_100.jpg"
    },

    {
        "name": "red tree",
        "price": 200,
        "currency": "rub",
        "picture": "bot/handlers/tree_200.jpg"
    },
]


async def logged_in(query: types.CallbackQuery, callback_data: AboutSrCallback) -> None:
    """

    :param query:
    :param callback_data:
    :return:
    """
    page = 1

    await query.message.delete()

    await query.message.answer_photo(
        photo=FSInputFile(items[page - 1]["picture"]),
        caption=templates.generate_store_page(
            name=items[page - 1]["name"],
            price=items[page - 1]["price"],
            currency=items[page - 1]["currency"]
        ),
        reply_markup=keyboards.store.generate(page, len(items))
    )

    await query.answer()


async def not_logged_in(query: types.CallbackQuery, callback_data: AboutSrCallback) -> None:
    """

    :param query:
    :param callback_data:
    :return:
    """
    page = 1

    await query.message.delete()

    await query.message.answer_photo(
        photo=FSInputFile(items[page-1]["picture"]),
        caption=templates.generate_store_page(
            name=items[page - 1]["name"],
            price=items[page - 1]["price"],
            currency=items[page - 1]["currency"]
        ),
        reply_markup=keyboards.store.generate(page, len(items))
    )

    await query.answer()


async def slider(query: types.CallbackQuery, callback_data: StoreCallback) -> None:
    """

    :param query:
    :param callback_data:
    :return:
    """
    page = callback_data.page

    if page > 0:
        await query.message.delete()

        await query.message.answer_photo(
            photo=FSInputFile(items[page - 1]["picture"]),
            caption=templates.generate_store_page(
                name=items[page - 1]["name"],
                price=items[page - 1]["price"],
                currency=items[page - 1]["currency"]
            ),
            reply_markup=keyboards.store.generate(page, len(items))
        )

    await query.answer()
