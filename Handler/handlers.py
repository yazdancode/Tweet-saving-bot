import telebot.types
from telebot import TeleBot
from Model.model import Student
from telebot.apihelper import ApiTelegramException
from typing import List, Dict, Union
from Enum.enum import BotMessages, ChannelInfo, BotCommands
from Callbacks.Callback.Tweet_Request.tweet_request import (
    tweet_request,
    support_handler,
)
from telebot.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def send_typing_action(bot: TeleBot, chat_id: Union[int, str]) -> None:
    bot.send_chat_action(chat_id, "typing")


def send_message_with_markup(
    bot: TeleBot,
    chat_id: Union[int, str],
    text: str,
    reply_markup: Union[ReplyKeyboardMarkup, InlineKeyboardMarkup, None] = None,
) -> None:
    send_typing_action(bot, chat_id)
    bot.send_message(chat_id, text=text, reply_markup=reply_markup)


def create_keyboard_markup(buttons: List[Dict[str, str]]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    for current_button_info in buttons:
        button = InlineKeyboardButton(**current_button_info)
        keyboard.add(button)
    return keyboard


def is_subscribed(
    bot: TeleBot, user_id: Union[int, str], channels: List[Union[int, str]]
) -> bool:
    try:
        for i in channels:
            is_member = bot.get_chat_member(chat_id=i, user_id=user_id)
            if is_member.status in ["kicked", "left"]:
                return False
        return True
    except ApiTelegramException as e:
        if e.result_json["description"] == "Bad Request: chat not found":
            return False
        return False


def is_user_registered(chat_id: Union[int, str]) -> bool:
    user = Student.get(chat_id=chat_id)
    return user is not None


def handle_start_command(bot: TeleBot, messages: Message) -> None:
    if is_user_registered(messages.from_user.id):
        keyboard = ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True, row_width=2
        )
        keyboard.add(
            KeyboardButton(ChannelInfo.create_request.value),
            KeyboardButton(BotCommands.GUIDE.value),
            KeyboardButton(
                BotCommands.MANUFACTURER.value,
            ),
            KeyboardButton(BotCommands.Search_request.value),
        )
        send_message_with_markup(
            bot,
            messages.chat.id,
            BotMessages.generate_starts_message(),
            reply_markup=keyboard,
        )
    else:
        buttons = [
            {
                "text": ChannelInfo.MEMBERSHIP.value,
                "callback_data": "membership",
            },
        ]
        keyboard = create_keyboard_markup(buttons)
        send_message_with_markup(
            bot,
            messages.chat.id,
            BotMessages.generate_channel_membership_message(),
            reply_markup=keyboard,
        )
    bot.delete_my_commands()
    bot.set_my_commands(
        commands=[
            telebot.types.BotCommand("start", "شروع ربات"),
            telebot.types.BotCommand("guide", "راهنمای ربات"),
            telebot.types.BotCommand("manufacturer", "ارتباط با سازنده ربات"),
        ]
    )

    @bot.message_handler(func=lambda received_message: True)
    def handle_keyboard(received_message: Message):
        text = received_message.text
        chat_id = received_message.chat.id
        if text == ChannelInfo.create_request.value:
            keyboards = ReplyKeyboardMarkup(
                resize_keyboard=True, one_time_keyboard=True, row_width=1
            )
            keyboards.add(BotMessages.SUBMIT_TEXT.value, BotMessages.COMING_BACK.value)
            bot.send_message(
                chat_id, BotMessages.TWEET_TEXT.value, reply_markup=keyboards
            )
        elif text == BotMessages.SUBMIT_TEXT.value:
            bot.send_message(chat_id, BotMessages.SUBMIT_REQUESTS.value)
            bot.register_next_step_handler(
                received_message, lambda message: tweet_request(message, bot)
            )
        elif text == BotCommands.MANUFACTURER.value:
            keyboards = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            keyboards.add(
                BotCommands.Communication__management.value,
                BotCommands.Programmer_resume.value,
                BotMessages.COMING_BACK.value,
                ChannelInfo.Order.value,
            )
            bot.send_message(
                chat_id, BotMessages.profiles.value, reply_markup=keyboards
            )
        elif text in [
            BotCommands.Communication__management.value,
            ChannelInfo.Order.value,
        ]:
            keyboards = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            keyboards.add(BotCommands.opt_out.value)
            bot.send_message(chat_id, BotMessages.text.value, reply_markup=keyboards)
            bot.register_next_step_handler(
                received_message, lambda message: support_handler(message, bot)
            )
        elif text == BotCommands.Programmer_resume.value:
            channel_username = "yazdancodeo"
            message_id = 26
            keyboards = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            keyboards.add(BotCommands.opt_out.value)
            bot.send_message(chat_id, BotMessages.profile.value, reply_markup=keyboards)
            bot.forward_message(
                chat_id, from_chat_id="@" + channel_username, message_id=message_id
            )
        elif text == BotCommands.GUIDE.value:
            keyboards = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            keyboards.add(BotMessages.COMING_BACK.value)
            bot.send_message(
                chat_id,
                ChannelInfo.guide.value,
                reply_markup=keyboards,
            )
        elif text == BotCommands.Search_request.value:
            keyboards = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            keyboards.add(BotMessages.COMING_BACK.value)
            bot.send_message(
                received_message.chat.id,
                ChannelInfo.error.value,
                reply_markup=keyboards,
            )
        elif text == BotMessages.COMING_BACK.value or text == BotCommands.opt_out.value:
            keyboards = ReplyKeyboardMarkup(
                resize_keyboard=True, one_time_keyboard=True, row_width=2
            )
            keyboards.add(
                KeyboardButton(ChannelInfo.create_request.value),
                KeyboardButton(BotCommands.GUIDE.value),
                KeyboardButton(BotCommands.MANUFACTURER.value),
                KeyboardButton(BotCommands.Search_request.value),
            )
            bot.send_message(
                chat_id, BotMessages.generate_back_message(), reply_markup=keyboards
            )


def guide_handler(bot: TeleBot, message: Message) -> None:
    send_message_with_markup(bot, message.chat.id, ChannelInfo.error.value)


def manufacturer_handler(bot: TeleBot, message: Message) -> None:
    keyboards = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboards.add(
        BotCommands.Communication__management.value,
        BotCommands.Programmer_resume.value,
        BotMessages.COMING_BACK.value,
        ChannelInfo.Order.value,
    )
    send_message_with_markup(
        bot, message.chat.id, BotMessages.profiles.value, reply_markup=keyboards
    )

    text = message.text
    chat_id = message.chat.id

    if text in [
        BotCommands.Communication__management.value,
        BotCommands.Programmer_resume.value,
    ]:
        keyboards = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        keyboards.add(BotCommands.opt_out.value)
        bot.send_message(
            chat_id,
            (
                BotMessages.text.value
                if text == BotCommands.Communication__management.value
                else BotMessages.profile.value
            ),
            reply_markup=keyboards,
        )
    elif text == BotCommands.opt_out.value:
        keyboards = ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True, row_width=2
        )
        keyboards.add(
            KeyboardButton(ChannelInfo.create_request.value),
            KeyboardButton(BotCommands.GUIDE.value),
            KeyboardButton(BotCommands.MANUFACTURER.value),
            KeyboardButton(BotCommands.Search_request.value),
        )
        bot.send_message(
            chat_id, BotMessages.generate_starts_message(), reply_markup=keyboards
        )
    elif text == ChannelInfo.Order.value:
        keyboards = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        keyboards.add(BotCommands.opt_out.value)
        bot.send_message(chat_id, BotMessages.text.value, reply_markup=keyboards)
        bot.register_next_step_handler(
            message, lambda messages: support_handler(message, bot)
        )
