import telebot

bot = telebot.TeleBot("6745385275:AAESHGHgt1wF1zBXtbQPvcJoNAaUQ79TXjU")


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello!")


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, f"id: {message.from_user.id}, username: {message.from_user.username}")


bot.polling(none_stop=True)
