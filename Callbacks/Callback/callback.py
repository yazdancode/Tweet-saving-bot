from telebot import TeleBot
from telebot.types import CallbackQuery

from Database.database import creat_student, create_tweet
from Enum.enum import BotResponses, Channel


def callback_handler(call: CallbackQuery, bot: TeleBot) -> None:
    if call.data == "channel":
        bot.send_message(call.message.chat.id, Channel.ID_CHANNEL.value)
    elif call.data == "membership":
        chat_id = call.message.chat.id
        user_id = call.from_user.id
        username = call.from_user.username
        first_name = call.from_user.first_name
        last_name = call.from_user.last_name

        try:
            member_status = bot.get_chat_member(chat_id, user_id).status
            if member_status in ["member", "administrator"]:
                creat_student(
                    username=username,
                    chat_id=chat_id,
                    first_name=first_name,
                    last_name=last_name,
                )
                bot.send_message(chat_id, text=BotResponses.START_HANDLER.value)
            else:
                bot.reply_to(call.message, Channel.WELCOME.value)
        except Exception as e:
            print("Error:", e)
            bot.reply_to(call.message, Channel.ERROR.value)


def text_button_handler() -> None:
    pass
