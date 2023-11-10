__all__ = ["generate_bot_commands"]

from typing import List

from aiogram.types import BotCommand

commands = (
    ("start", "Команда для начала работы с ботом."),
    ("cancel", "Команда для отмены действия."),
    ("help", "Команда для помощи.")
)


def generate_bot_commands() -> List[BotCommand]:
    """

    :return:
    """
    bot_commands = []

    for cmd, desc in commands:
        bot_commands.append(BotCommand(command=cmd, description=desc))

    return bot_commands
