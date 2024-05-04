from enum import Enum


class BotResponses(Enum):
    Channel_membership = (
        "سلام به ربات دانشگاه لرستان خوش آمدید خوش آمدید,"
        " راه اندازی ربات در کانال عضو باشید."
    )
    START_HANDLER = "به ربات درخواست دانشجو خوش آمدید."
    SUBMIT_REQUESTS = "لطفاً درخواست خود را بنویسید:"
    MEMBERS_OFF = "لطفاً نوع درخواست خود را وارد کنید:"
    SUBMIT_REQUEST = "ثبت توییت ✅"


class BotCommands(Enum):

    START = "راه اندازی ربات"
    REQUESTS = "ارسال درخواست"
    GUIDE = "راهنما ربات"
    MANUFACTURER = "سازنده ربات"


class Channel(Enum):
    CHANNEL = "کانال"
    MEMBERSHIP = "عضویت ✅"
    ID_CHANNEL = "https://t.me/sedayedaneshjoo_lu"
    DESCRIPTION = "به کانال ما بپیوندید!"
    ERROR = "خطایی رخ داده است. لطفاً دوباره امتحان کنید."
    WELCOME = "شما عضو کانال نیستید. برای استفاده از ربات باید عضو کانال باشید"
    ROBOT_GUIDE = """با سلام 
این اصلی این ربات اینه که درخواست های دانشجو رو ثبت می‌کنه و در گروه منتشر می‌کنه
با تشکر."""


class Keys(Enum):
    lost = "گم شده"
    found = "پیدا شده"
    announcement = "اعلامیه"
    survey = "نظرسنجی"
    tweet = "توییت"
