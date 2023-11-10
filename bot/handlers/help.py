from aiogram.types import Message


async def help_command(message: Message) -> None:
    """
    Хэндлер для команды /help
    :param message:
    :return:
    """
    await message.answer("Команда для помощи.\nНажми -> /start")
