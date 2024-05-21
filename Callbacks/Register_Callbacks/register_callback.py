from telebot import TeleBot
from Callbacks import callback


def register_callback_handler(bot: TeleBot) -> None:
    callback_prefixes = [
        "membership",
        "tweet",
        "guide",
        "manufacture",
        "cancel",
    ]
    for prefix in callback_prefixes:
        bot.register_callback_query_handler(
            callback=callback.handle_channel_callback,
            func=lambda call, p=prefix: call.data.startswith(p),
            pass_bot=True,
        )
    bot.register_callback_query_handler(
        callback=callback.confirmation_handler,
        func=lambda call: call.data.startswith("confirm:"),
        pass_bot=True,
    )
