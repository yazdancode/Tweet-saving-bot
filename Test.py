import telebot

bot = telebot.TeleBot("6762756076:AAGfjoGZmF-bHAsmRGOHGvNO1ITLHWwb8Ws")

first_button = telebot.types.InlineKeyboardButton(
    "Button 1", url="https://www.google.com/"
)
second_button = telebot.types.InlineKeyboardButton("Button 2", callback_data="hi")
markup = telebot.types.InlineKeyboardMarkup()
markup.add(first_button, second_button)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    bot.reply_to(call.message, text="You clicked on the Hi button")


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.chat.id, text="Hi", reply_markup=markup)


if __name__ == "__main__":
    bot.infinity_polling()
