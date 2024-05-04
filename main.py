import telebot
from decouple import config
from telebot.types import Message
from Callbacks import Register_Handlers
from Model.model import create_db_and_tables
from Handler.handlers import handle_start_command, guide_handler, manufacturer_handler


TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")
ID_CHANNEL = config("ID_CHANNEL")
bot = telebot.TeleBot(TELEGRAM_TOKEN)
Register_Handlers.register_all_handlers(bot)


def start_bot() -> None:

    @bot.message_handler(commands=["start"])
    def handle_start(message: Message) -> None:
        handle_start_command(bot, messages=message)


def guide_bot() -> None:

    @bot.message_handler(commands=["guide"])
    def handle_guide(message: Message) -> None:
        guide_handler(bot, message=message)


def manufacturer_bot() -> None:
    @bot.message_handler(commands=["manufacturer"])
    def handle_manufacturer(message: Message) -> None:
        manufacturer_handler(bot, message=message)


def initialize_bot() -> None:
    start_bot()
    guide_bot()
    manufacturer_bot()
    create_db_and_tables()


if __name__ == "__main__":
    initialize_bot()
    bot.polling(none_stop=True)
