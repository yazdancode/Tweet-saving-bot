from telebot import TeleBot

from Callbacks.Callback.callback import callback_handler, text_button_handler


def register_callback_handler(bot: TeleBot) -> None:
    bot.register_callback_query_handler(
        callback=callback_handler,
        func=lambda call: call.data.startswith("channel"),
        pass_bot=True,
    )
    bot.register_callback_query_handler(
        callback=callback_handler,
        func=lambda call: call.data.startswith("membership"),
        pass_bot=True,
    )
    bot.register_callback_query_handler(
        callback=text_button_handler,
        func=lambda call: call.data.startswith("text_button"),
        pass_bot=True,
    )
