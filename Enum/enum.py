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

    SUBMIT_REQUESTS = "لطفاً درخواست خود را بنویسید:"
    SUBMIT_REQUEST = "ثبت توییت ✅"
    SUBMIT_TEXT = "نوشتن متن"
    SUBMIT_MATAN = "توییت"
    DELETE_TEXT = "حذف توییت"
    TWEET_TEXT = "برای نوشتن توییتت خود روی گزینه نوشتن متن زیر کلیک کنید :"
    COMING_BACK = "بازگشت"
    profile = (
        "┬\n [❤️ Profile ]"
        "\n│├ 👤 name : Yazdan"
        "\n│├ 🆔 Username : @Y_Shabanei"
        "\n│├ 🤙 PhoneNumber : 09102779237"
        "\n│└ 📱 UserID : 5105508285"
        "\n│├┬ [✅ Personal Info ]"
        "\n│├ 👤 First Name : Yazdan"
        "\n│├ ✍️ Last Name : Shabanei"
        "\n│├ 👤 Student : electrical engineering"
        "\n│├ 🗓 Date Of Birth : 1999"
        "\n│└ 📍 Location : Iran,Tehran "
        "\n│├┬ [🎓 Skill ]"
        "\n│└ 📝 python"
        "\n│├┬ [ 💬 Social Media ]"
        "\n│├ 🧐 Instagram"
        "\n│├ 😔 WhatsApp"
        "\n│├ 💼 Linkedin"
        "\n│└ 🐙 GitHub"
        "\n│├┬ [⌨️ More ]"
        "\n│├  Apprentice programmer: Snap"
        "\n│├ 🤖 Bot : Not Available"
        "\n│├ ⭐️ WebSite : yazdancode.com"
        "\n│├ 💬 Group : Not Available"
        "\n│└ 📣 Channel : @yazdancodeo"
        "\n│└✅"
    )


class BotCommands(Enum):
    START = "راه اندازی ربات"
    GUIDE = "راهنما ربات"
    MANUFACTURER = "ارتباط با سازنده ربات"
    Search_request = "جستجو"


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
