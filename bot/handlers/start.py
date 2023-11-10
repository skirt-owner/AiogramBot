from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

from bot import templates, keyboards


web_app_button = KeyboardButton(text="STORE", web_app=WebAppInfo(url="https://qihangfan.github.io/index.html"))
web_app_keyboard = ReplyKeyboardMarkup(
    keyboard=[[web_app_button]],
    row_width=1,
    resize_keyboard=True
)


async def not_logged_in_start(
        message: Message,
        state: FSMContext
) -> None:
    """
    Хэндлер для команды /start
    :param state:
    :param message:
    :return:
    """
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()

    await message.answer(
        text=templates.start.not_logged_in,
        reply_markup=keyboards.start.not_logged_in
    )


async def logged_in_start(
        message: Message,
        state: FSMContext
) -> None:
    """
    Хэндлер для команды /start
    :param state:
    :param message:
    :return:
    """
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()

    await message.answer(
        text=templates.start.logged_in,
        reply_markup=keyboards.start.logged_in
    )
