from telebot import types

start_markup = types.ReplyKeyboardMarkup()
start_markup.add(types.KeyboardButton("Старт"))

stop_markup = types.ReplyKeyboardMarkup()
stop_markup.add(types.KeyboardButton("Стоп"))
