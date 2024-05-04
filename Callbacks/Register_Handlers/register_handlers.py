from telebot import TeleBot

from Callbacks.Register_Callbacks.register_callback import register_callback_handler
from Enum.enum import BotCommands
from Handler import handlers


def register_command_handler(bot: TeleBot) -> None:
    bot.register_message_handler(
        handlers.start_handler, commands=[BotCommands.START.value], pass_bot=True
    )
    bot.register_message_handler(
        handlers.request_handler, commands=[BotCommands.REQUESTS.value], pass_bot=True
    )
    bot.register_message_handler(
        handlers.guide_handler, commands=[BotCommands.GUIDE.value], pass_bot=True
    )
    bot.register_message_handler(
        handlers.manufacturer_handler,
        commands=[BotCommands.MANUFACTURER.value],
        pass_bot=True,
    )


def register_callback_query_handler(bot: TeleBot) -> None:
    register_callback_handler(bot)


def register_all_handlers(bot: TeleBot) -> None:
    register_command_handler(bot)
    register_callback_query_handler(bot)
