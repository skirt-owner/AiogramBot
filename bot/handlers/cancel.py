from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot import templates, keyboards

router = Router()


async def cancel_callback_logged_in(
        query: CallbackQuery,
        state: FSMContext
) -> None:
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()

    await query.message.delete()

    await query.message.answer(
        text=templates.start.logged_in,
        reply_markup=keyboards.start.logged_in
    )

    await query.answer(
        text="Отмена действия"
    )


async def cancel_callback_not_logged_in(
        query: CallbackQuery,
        state: FSMContext
) -> None:
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()

    await query.message.delete()

    await query.message.answer(
        text=templates.start.not_logged_in,
        reply_markup=keyboards.start.not_logged_in
    )

    await query.answer(
        text="Отмена действия"
    )


async def cancel_command_not_logged_in(
        message: Message,
        state: FSMContext
) -> None:
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()

    await message.answer(
        text=templates.start.not_logged_in,
        reply_markup=keyboards.start.not_logged_in
    )


async def cancel_command_logged_in(
        message: Message,
        state: FSMContext
) -> None:
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()

    await message.answer(
        text=templates.start.logged_in,
        reply_markup=keyboards.start.logged_in
    )
