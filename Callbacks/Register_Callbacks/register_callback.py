from telebot import TeleBot
from Callbacks import callback


def register_callback_handler(bot: TeleBot) -> None:
    callback_prefixes = [
        "membership",
        "tweet",
        "request",
        "guide",
        "manufacture",
        "confirm",
    ]
    for prefix in callback_prefixes:
        bot.register_callback_query_handler(
            callback=callback.handle_channel_callback,
            func=lambda call, p=prefix: call.data.startswith(p),
            pass_bot=True,
        )
