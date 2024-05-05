from typing import Callable, Optional
from sqlmodel import Field
from telebot import TeleBot
from telebot.types import CallbackQuery, ReplyKeyboardMarkup

from Config import configs
from Enum.enum import BotMessages, BotCommands, ChannelInfo
from Handler.handlers import guide_handler, manufacturer_handler, is_subscribed
from Model.model import Student, Tweet, ApprovedRequest, Admin

CALLBACK_MEMBERSHIP: str = "membership"
CALLBACK_GUIDE: str = "guide"
CALLBACK_MANUFACTURE: str = "manufacture"
CALLBACK_CONFIRM: str = "confirm"
ActionType = Callable[[], None]


def handle_channel_callback(call: CallbackQuery, bot: TeleBot) -> None:
    actions: dict[str, ActionType] = {
        CALLBACK_MEMBERSHIP: lambda: handle_membership_request(call, bot),
        CALLBACK_GUIDE: lambda: guide_handler(bot, call.message),
        CALLBACK_MANUFACTURE: lambda: manufacturer_handler(bot, call.message),
        CALLBACK_CONFIRM: lambda: confirmation_handler(call, bot),
    }

    action: Optional[ActionType] = actions.get(call.data)
    if action:
        action()


def create_keyboard(buttons: list[str], row_width: int = 2) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True, row_width=row_width
    )
    for button in buttons:
        keyboard.add(button)
    return keyboard


def handle_membership_request(call: CallbackQuery, bot: TeleBot) -> None:
    is_member: bool = is_subscribed(
        bot, user_id=call.from_user.id, channels=configs.channels
    )
    if is_member is False:
        bot.answer_callback_query(call.id, ChannelInfo.WELCOME.value, show_alert=True)
    elif is_member:
        student: Optional[Student] = Student.get(chat_id=call.from_user.id)
        if student is None:
            users = call.from_user
            user = users.username if users.username else "UnknownUserName"
            last_name = users.last_name if users.last_name else "UnknownLastName"
            first_name = users.first_name if users.first_name else "UnknownFirstName"
            chat_id = call.message.chat.id
            Student.create_student(
                username=user,
                chat_id=chat_id,
                last_name=last_name,
                first_name=first_name,
            )
            keyboard_buttons = [
                ChannelInfo.create_request.value,
                BotCommands.GUIDE.value,
                BotCommands.MANUFACTURER.value,
                BotCommands.Search_request.value,
            ]
            keyboard = create_keyboard(keyboard_buttons)
            bot.send_message(
                call.message.chat.id,
                BotMessages.generate_start_message(),
                reply_markup=keyboard,
            )
        else:
            keyboard_buttons = [
                ChannelInfo.create_request.value,
                BotCommands.GUIDE.value,
                BotCommands.MANUFACTURER.value,
                BotCommands.Search_request.value,
            ]
            keyboard = create_keyboard(keyboard_buttons)
            bot.send_message(
                call.message.chat.id,
                BotMessages.generate_starts_message(),
                reply_markup=keyboard,
            )
def confirmation_handler(call: CallbackQuery, bot: TeleBot) -> None:
    admin = Admin.get(username=call.from_user.username)
    student = Student.get(chat_id=call.message.chat.id)
    tweet = Tweet.get(chat_id=call.message.chat.id)
    if tweet:
        chat_id = tweet.chat_id
        first_name = tweet.first_name
        last_name = tweet.last_name
        content = tweet.content
        ApprovedRequest.create_approvedrequest(
            chat_id=chat_id,
            first_name=first_name,
            last_name=last_name,
            content=content,
        )
    else:
        if admin:
            chat_id = call.message.chat.id
            bot.send_message(chat_id, "توییتی با این شناسه یافت نشد.")
        else:
            pass
        if student:
             bot.send_message(student.chat_id, "درخواست شما توسط ادمین تأیید شد ✅")
        else:
            bot.send_message(student.chat_id, "دانش‌آموزی با این یوزرنیم یافت نشد.")


# def handle_edit_request(call: CallbackQuery, bot: TeleBot) -> None:
#     pass
#
#
# def handle_cancel(call: CallbackQuery, bot: TeleBot) -> None:
#     pass
