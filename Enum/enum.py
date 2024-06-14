from enum import Enum
from decouple import config


def generate_message(*args):
    """

    :param args:
    :type args:
    :return:
    :rtype:
    """
    return "\n".join(args)


class BotMessages(Enum):
    @staticmethod
    def generate_channel_membership_message():
        """

        :return:
        :rtype:
        """
        return generate_message(
            "☑️ برای استفاده از ربات ««صدای دانشجو دانشگاه لرستان» ابتدا باید وارد کانال «صدای دانشجو دانشگاه لرستان» شوید.",
            "❗️ برای جدیدترین اخبار دانشگاه, اطلاعیه ها و گزارشات , فایل‌های آموزشی مورد نیاز دانشجو شما باید عضو کانال شوید: "
            "",
            "",
            "📣  کانال: @yazdancodeo",
            "",
            "👇 بعد از عضویت در کانال روی دکمه « ✅ تایید عضویت » بزنید 👇",
        )

    @staticmethod
    def generate_starts_message():
        """

        :return:
        :rtype:
        """
        return generate_message(
            "  سلام به ربات درخواست دانشجو خوش آمدید.✋",
            "",
            "با ربات ثبت درخواست همراه شماییم تا به راحتی درخواست های شما ثبت کنیم.",
            "",
            "👇🏻 برای ادامه یکی از دکمه های زیر را انتخاب نمایید:",
        )

    @staticmethod
    def generate_start_message():
        """
        :return:
        :rtype:
        """
        return generate_message(
            "☑️ عضویت شما در کانال تایید شد.",
            "🌟 به ربات درخواست دانشجو خوش آمدید.",
            "👇🏻 برای ادامه یکی از دکمه های زیر را انتخاب نمایید:",
        )

    @staticmethod
    def generate_back_message():
        return generate_message(
            "✅کاربر عزیز شما به منوی اصلی بازگشتید",
            "",
            "👇🏻 برای ادامه یکی از دکمه های زیر را انتخاب نمایید:",
        )

    SUBMIT_REQUESTS = "لطفاً درخواست خود را بنویسید:"
    SUBMIT_REQUEST = "ثبت توییت ✅"
    SUBMIT_TEXT = "نوشتن متن"
    SUBMIT_MATAN = "توییت"
    DELETE_TEXT = "حذف توییت"
    TWEET_TEXT = "برای نوشتن توییت خود روی گزینه نوشتن متن زیر کلیک کنید :"
    COMING_BACK = "بازگشت"
    profile = "سلام کاربر گرامی\n " "رزومه برنامه نویس به شرح زیر است :"
    profiles = (
        "🔰 برای ارتباط مستقیم با ایدی زیر در ارتباط باشید :\n\n"
        "🆔 @Y_Shabanei"
        "\n\n⚖️ کاربر گرامی، چنانچه شما از ربات"
        "\n(صدای دانشجو دانشگاه لرستان) استفاده نمایید به منزله قبول قوانین است 👇\n\n"
        "1⃣ سعی بخش پشتیبانی بر این است که تمامی پیام های دریافتی در کمتر از 24 \n"
        "ساعت پاسخ داده شوند، بنابراین تا زمان دریافت پاسخ صبور باشید.\n\n"
        "2⃣ خرید و فروش موجودی ربات توسط کاربران ممنوعیتی ندارد اما صدای دانشجو دانشگاه لرستان هیچ گونه تعهدی در این رابطه ندارد. \n\n"
        "3⃣ چنانچه تراکنش مشکوکی رخ دهد صدای دانشجو  این را دارد از کاربر مورد نظر مدارک مربوطه را بگیرد.\n\n"
        "✅ لطفا موضوع پیام ارسال خود را انتخاب کنید"
    )
    text = (
        "• لطفا پیام خود را در قالب یک پیام ارسال کنید\n\n"
        "• پیام شما برای مدیریت اصلی ربات ارسال خواهد شد"
    )


class BotCommands(Enum):
    START = "راه اندازی ربات"
    GUIDE = "راهنما ربات"
    MANUFACTURER = "ارتباط با سازنده ربات"
    Search_request = "جستجو"
    Communication__management = "ارتباط با مدیریت"
    Programmer_resume = "رزومه برنامه نویس"
    opt_out = "انصراف"


class ChannelInfo(Enum):
    MEMBERSHIP = " تایید عضویت ✅"
    ID_CHANNEL = config("ID_CHANNEL")
    ERROR = "خطایی رخ داده است. لطفاً دوباره امتحان کنید."
    WELCOME = "❌ هنوز داخل کانال «@sedayedaneshjoo_lu» عضو نیستی"
    Telegram_Text = generate_message(
        "درخواست شما با موفقیت به ادمین ارسال شد.",
        " پس از بررسی نتیجه به شما اعلام خواهد شد.",
    )
    create_request = "ایجاد درخواست"
    error = "❌ خطا این بخش در هنوز طراحی ایجاد نشده است"
    Order = "ثبت سفارش"
    guide = "\nجهت مشکل به ایدی زیر مراجه کنید👇👇👇👇" "\n@Y_Shabanei"


class CallbackDate(Enum):
    CALLBACK_MEMBERSHIP: str = "membership"
    CALLBACK_GUIDE: str = "guide"
    CALLBACK_MANUFACTURE: str = "manufacture"
    CALLBACK_CONFIRM: str = "confirm"
    CALLBACK_CANCEL: str = "cancel"
