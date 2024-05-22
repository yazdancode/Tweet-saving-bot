from datetime import datetime
from decouple import config
from persiantools.jdatetime import JalaliDate
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, Message, InlineKeyboardButton
from Config import configs
from Enum.enum import ChannelInfo
from Model.model import Tweet, Admin


def tweet_request(message: Message, bot: TeleBot) -> None:
    username: str = message.from_user.username
    chat_id: int = message.chat.id
    first_name: str = message.chat.first_name or "نام نامشخص"
    last_name: str = message.chat.last_name or "نام خانوادگی وجود ندارد"
    user_text: str = message.text.strip()
    telegram_chat_id: str = config("TELEGRAM_CHAT_ID_ADMIN")
    current_date: datetime = datetime.today()
    jalali_date: str = JalaliDate(current_date).strftime("%Y/%m/%d")

    username_msg = (
        f"یوزرنیم: @{username}" if username else "یوزرنیم: نام کاربری وجود ندارد"
    )

    new_request_msg: str = (
        f"یک درخواست جدید دریافت شد\nاطلاعات کاربر به شرح زیر است:\n"
        f"محتوای درخواست: {user_text}\n"
        f"تاریخ ارسال: {jalali_date}\n"
        f"نام: {first_name}\n"
        f"نام خانوادگی: {last_name}\n"
        f"{username_msg}\n"
        f"شماره کاربری: {chat_id}\n"
        "دریافت شد. "
    )
    bot.send_message(telegram_chat_id, text=new_request_msg, parse_mode="html")
    Tweet.create_tweet(
        chat_id=chat_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        content=user_text,
        postage_date=jalali_date,
    )
    bot.send_message(chat_id, ChannelInfo.Telegram_Text.value)
    bot.delete_state(user_id=message.from_user.id, chat_id=message.chat.id)
    Admin.create_admin_once()
    Admin.update_admin_monthly()

    review_keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton("تایید درخواست ✅", callback_data=f"confirm:{chat_id}"),
        InlineKeyboardButton("لغو درخواست ❌", callback_data=f"cancel:{chat_id}"),
    ]
    review_keyboard.add(*buttons)

    review_message = bot.send_message(
        telegram_chat_id,
        "لطفا درخواست را با دقت بررسی کنید:",
        reply_markup=review_keyboard,
    )

    configs.pending_review_requests[message.from_user.id] = {
        "message": review_message,
        "keyboard": review_keyboard,
    }


def send_response_to_user(message_text: str, user_chat_id: int, bot: TeleBot):
    bot.send_message(chat_id=user_chat_id, text=message_text)


def support_handler(message: Message, bot: TeleBot):
    chat_id: int = message.chat.id
    user_text: str = message.text.strip()
    robot_marker: str = config("ROBOT_MARKER")

    bot.send_message(chat_id=robot_marker, text=f"پیام از کاربر:\n{user_text}")
    bot.reply_to(message, "✅ پیام شما با موفقیت به پشتیبانی ارسال شد.")

    creator_reply = (
        "پیام شما با موفقیت به پشتیبانی ارسال شد و به زودی جواب آن ارسال خواهد شد."
    )
    send_response_to_user(creator_reply, chat_id, bot)
