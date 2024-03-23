from telebot import types

start_markup = types.ReplyKeyboardMarkup()
start_markup.add(types.KeyboardButton("Старт"))

stop_markup = types.ReplyKeyboardMarkup()
stop_markup.add(types.KeyboardButton("Стоп"))

save_markup = types.ReplyKeyboardMarkup()
save_markup.add(types.KeyboardButton("Сохранить сборку"))
save_markup.add(types.KeyboardButton("Пропустить сборку"))


repeat_markup = types.ReplyKeyboardMarkup()
repeat_markup.add(types.KeyboardButton("Следующая сборка"))
repeat_markup.add(types.KeyboardButton("Вернуться в меню"))
