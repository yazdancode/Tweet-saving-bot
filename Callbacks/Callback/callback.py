from typing import Callable, Optional

from telebot import TeleBot
from telebot.types import CallbackQuery, ReplyKeyboardMarkup
from Config import configs
from Enum.enum import BotMessages, BotCommands, ChannelInfo, CallbackDate
from Handler.handlers import guide_handler, manufacturer_handler, is_subscribed
from Model.model import Student

ActionType = Callable[[], None]


def handle_channel_callback(call: CallbackQuery, bot: TeleBot) -> None:
    actions: dict[str, ActionType] = {
        CallbackDate.CALLBACK_MEMBERSHIP.value: lambda: handle_membership_request(
            call, bot
        ),
        CallbackDate.CALLBACK_GUIDE.value: lambda: guide_handler(bot, call.message),
        CallbackDate.CALLBACK_MANUFACTURE.value: lambda: manufacturer_handler(
            bot, call.message
        ),
        CallbackDate.CALLBACK_CONFIRM.value: lambda: confirmation_handler(call, bot),
        CallbackDate.CALLBACK_CANCEL.value: lambda: handle_cancel(call, bot),
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
    pass


# def handle_edit_request(call: CallbackQuery, bot: TeleBot) -> None:
#     pass


def handle_cancel(call: CallbackQuery, bot: TeleBot) -> None:
    pass
