from telebot.types import InlineKeyboardMarkup, Message, InlineKeyboardButton
from telebot import TeleBot
from decouple import config
from Enum.enum import ChannelInfo
from Model.model import Tweet, Admin
from Config import configs


def tweet_request(message: Message, bot: TeleBot) -> None:
    chat_id: int = message.chat.id
    first_name: str = message.chat.first_name or "UnknownFirstName"
    last_name: str = message.chat.last_name or "UnknownLastName"
    user_text: str = message.text.strip()
    telegram_chat_id: str = config("TELEGRAM_CHAT_ID_ADMIN")
    Tweet.create_tweet(
        chat_id=chat_id,
        first_name=first_name,
        last_name=last_name,
        content=user_text,
    )
    bot.send_message(chat_id, ChannelInfo.Telegram_Text.value)
    Admin.create_admin_once()
    Admin.update_admin_monthly()
    new_request_msg: str = (
        f"یک درخواست جدید از طرف کاربر"
        f"<ins>{first_name}</ins> "
        f"با ایدی تگرامی "
        f"<ins>{chat_id}</ins> "
        "دریافت شد "
        "متن درخواست :"
        f"{str(user_text)}"
    )
    bot.send_message(telegram_chat_id, text=new_request_msg, parse_mode="html")
    review_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup()
    confirm_button: InlineKeyboardButton = InlineKeyboardButton(
        "تایید درخواست ✅", callback_data=f"confirm"
    )
    edit_button: InlineKeyboardButton = InlineKeyboardButton(
        "درخواست ویرایش ✏️", callback_data=f"edit_"
    )
    cancellation_button: InlineKeyboardButton = InlineKeyboardButton(
        "لغو درخواست ❌", callback_data=f"cancel_"
    )
    review_keyboard.add(confirm_button, edit_button, cancellation_button)
    review_message = bot.send_message(
        telegram_chat_id,
        "لطفا درخواست را با دقت بررسی کنید:",
        reply_markup=review_keyboard,
    )
    configs.pending_review_requests[message.from_user.id] = {
        "message": review_message,
        "keyboard": review_keyboard,
    }