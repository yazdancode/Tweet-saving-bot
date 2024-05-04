import telebot
from decouple import config
from telebot.types import Message

from Callbacks.Register_Handlers import register_all_handlers
from Handler.handlers import (
    guide_handler,
    manufacturer_handler,
    request_handler,
    start_handler,
)
from Model.model import create_db_and_tables

TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")
STUDENT_GROUP_CHAT_ID = config("STUDENT_GROUP_CHAT_ID")
ID_CHANNEL = config("ID_CHANNEL")
bot = telebot.TeleBot(TELEGRAM_TOKEN)
register_all_handlers(bot)


def start_bot() -> None:
    """دستورکار دستور شروع را راه‌اندازی کنید."""

    @bot.message_handler(commands=["start"])
    def handle_start(message: Message) -> None:
        start_handler(bot, message=message)


def request_bot() -> None:
    """دستورگر فرمان درخواست را راه‌اندازی کنید."""

    @bot.message_handler(commands=["request"])
    def handle_request(message: Message) -> None:
        request_handler(bot, message=message)


def guide_bot() -> None:
    """دستورگر فرمان راهنما را راه‌اندازی کنید."""

    @bot.message_handler(commands=["guide"])
    def handle_guide(message: Message) -> None:
        guide_handler(bot, message=message)


def manufacturer_bot() -> None:
    @bot.message_handler(commands=["manufacturer"])
    def handle_manufacturer(message: Message) -> None:
        manufacturer_handler(bot, message=message)


def initialize_bot() -> None:
    start_bot()
    request_bot()
    guide_bot()
    manufacturer_bot()
    create_db_and_tables()


if __name__ == "__main__":
    initialize_bot()
    bot.polling(none_stop=True)
