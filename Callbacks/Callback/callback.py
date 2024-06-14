from typing import Callable, Optional
from telebot import TeleBot
from telebot.types import CallbackQuery, ReplyKeyboardMarkup
from Config import configs
from Enum.enum import BotMessages, BotCommands, ChannelInfo, CallbackDate
from Handler.handlers import guide_handler, manufacturer_handler, is_subscribed
from Model.model import Student, Tweet, ApprovedRequest

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
    if not is_member:
        bot.answer_callback_query(call.id, ChannelInfo.WELCOME.value, show_alert=True)
    else:
        student: Optional[Student] = Student.get(chat_id=call.from_user.id)
        if student is None:
            users = call.from_user
            user = users.username if users.username else "نام کاربری وجود ندارد"
            last_name = (
                users.last_name if users.last_name else "نام خانوادگی وجود ندارد"
            )
            first_name = users.first_name if users.first_name else "نام نامشخص"
            chat_id = call.message.chat.id
            Student.create_student(
                username=user,
                chat_id=chat_id,
                last_name=last_name,
                first_name=first_name,
            )
            bot.send_message(
                chat_id,
                BotMessages.generate_start_message(),
                reply_markup=create_keyboard(
                    [
                        ChannelInfo.create_request.value,
                        BotCommands.GUIDE.value,
                        BotCommands.MANUFACTURER.value,
                        BotCommands.Search_request.value,
                    ]
                ),
            )
        else:
            bot.send_message(
                call.message.chat.id,
                BotMessages.generate_starts_message(),
                reply_markup=create_keyboard(
                    [
                        ChannelInfo.create_request.value,
                        BotCommands.GUIDE.value,
                        BotCommands.MANUFACTURER.value,
                        BotCommands.Search_request.value,
                    ]
                ),
            )


def confirmation_handler(call: CallbackQuery, bot: TeleBot) -> None:
    """
    Handle the confirmation of membership requests.

    :param call: CallbackQuery object containing the callback data
    :param bot: TeleBot object for interacting with the Telegram API
    """
    latest_request = Tweet.get_latest_request()
    user = call.data.split()[0]
    number = "".join([char for char in user if char.isdigit()])
    chat_id = int(number)
    user_info = bot.get_chat(chat_id)
    username = user_info.username if user_info.username else "نام کاربری وجود ندارد"
    first_name = user_info.first_name if user_info.first_name else "نام نامشخص"
    last_name = (
        user_info.last_name if user_info.last_name else "نام خانوادگی وجود ندارد"
    )
    content = latest_request.content
    ApprovedRequest.create_approved_request(
        chat_id=chat_id,
        first_name=first_name,
        last_name=last_name,
        username=username,
        content=content,
    )
    bot.send_message(chat_id, "درخواست شما توسط ادمین تأیید شد ✅")
    bot.send_message(call.message.chat.id, "🚀 پیام درخواست شما به کاربر ارسال شد")


# def handle_edit_request(call: CallbackQuery, bot: TeleBot) -> None:
#     pass


def handle_cancel(call: CallbackQuery, bot: TeleBot) -> None:
    user = call.data.split()[0]
    admin_message = call.message.chat.id
    number = "".join([char for char in user if char.isdigit()])
    chat_id = int(number)
    bot.send_message(chat_id, "درخواست شما توسط ادمین رد شد ❌")
    bot.send_message(admin_message, "پیام درخواست شما به کاربر ارسال شد")
