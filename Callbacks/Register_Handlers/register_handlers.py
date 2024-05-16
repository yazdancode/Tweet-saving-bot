from telebot import TeleBot

from Callbacks import Register_Callbacks
from Enum.enum import BotCommands
from Handler import handlers


def register_command_handler(bot: TeleBot) -> None:
    command_handlers = [
        (handlers.handle_start_command, BotCommands.START.value),
        (handlers.guide_handler, BotCommands.GUIDE.value),
        (handlers.manufacturer_handler, BotCommands.MANUFACTURER.value),
    ]

    for handler, command in command_handlers:
        bot.register_message_handler(handler, commands=[command], pass_bot=True)


def register_callback_query_handler(bot: TeleBot) -> None:
    Register_Callbacks.register_callback_handler(bot)


def register_all_handlers(bot: TeleBot) -> None:
    register_command_handler(bot)
    register_callback_query_handler(bot)
