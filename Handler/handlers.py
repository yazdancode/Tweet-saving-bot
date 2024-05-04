from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from Enum.enum import BotResponses, Channel


def start_handler(bot: TeleBot, message: Message) -> None:
    bot.send_chat_action(message.chat.id, "typing")
    keyboard = InlineKeyboardMarkup(row_width=1)

    channel_button = InlineKeyboardButton(
        text=Channel.CHANNEL.value,
        callback_data="channel",
        url=Channel.ID_CHANNEL.value,
    )
    membership_button = InlineKeyboardButton(
        text=Channel.MEMBERSHIP.value, callback_data="membership"
    )

    keyboard.add(channel_button, membership_button)

    bot.reply_to(
        message, text=BotResponses.Channel_membership.value, reply_markup=keyboard
    )


def request_handler(bot, message):
    chat_id = message.chat.id
    bot.send_message(chat_id, text=BotResponses.SUBMIT_REQUESTS.value)


def guide_handler(bot: TeleBot, message: Message) -> None:
    chat_id = message.chat.id
    bot.send_message(chat_id, text=Channel.ROBOT_GUIDE.value)


def manufacturer_handler(bot: TeleBot, message: Message) -> None:
    chat_id = message.chat.id
    bot.send_message(chat_id, f"Your Telegram ID is: {chat_id}")
