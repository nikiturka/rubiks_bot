import time
import telebot
from sqlalchemy import select, insert
from markups import stop_markup, start_markup, repeat_markup, save_markup
from src.database import create_tables, session_factory
from src.models import User, Solve

bot = telebot.TeleBot("6745385275:AAESHGHgt1wF1zBXtbQPvcJoNAaUQ79TXjU")

create_tables()


@bot.message_handler(commands=['start'])
def start(message):
    with session_factory() as session:
        # try to find user in database
        query = select(User).where(User.username == message.from_user.username)
        user = session.execute(query).scalar()

        # create new user if not found
        if user is None:
            stmt = insert(User).values(username=message.from_user.username)
            session.execute(stmt)
            session.commit()

            bot.send_message(message.chat.id, f"Hello!, {message.from_user.username}")
        else:
            bot.send_message(message.chat.id, f"Hello, {user.username}!")


@bot.message_handler(commands=['scramble'])
def scramble(message):
    bot.send_message(message.chat.id, "Нажмите кнопку 'Start', чтобы запустить таймер.", reply_markup=start_markup)


@bot.message_handler(func=lambda message: message.text == "Старт")
def handle_start(message):
    start_time = time.time()
    bot.send_message(message.chat.id, "Таймер запущен!", reply_markup=stop_markup)
    bot.register_next_step_handler(message, lambda msg: handle_stop(msg, start_time))


@bot.message_handler(func=lambda message: message.text == "Стоп")
def handle_stop(message, s_time):
    stop_time = time.time() - s_time
    bot.send_message(message.chat.id, f"Ваше время: {stop_time:.2f} секунд.", reply_markup=save_markup)
    bot.register_next_step_handler(message, lambda msg: handle_save_or_skip(msg, stop_time))


def handle_save_or_skip(message, stop_time):
    if message.text == "Сохранить сборку":
        handle_save(message, stop_time)
    elif message.text == "Пропустить сборку":
        handle_skip(message)
    else:
        bot.send_message(message.chat.id, "Некорректный выбор. Пожалуйста, используйте кнопки для выбора действия.")


@bot.message_handler(func=lambda message: message.text == "Пропустить сборку")
def handle_skip(message):
    bot.send_message(message.chat.id, f"Сборка не была сохранена.", reply_markup=repeat_markup)


@bot.message_handler(func=lambda message: message.text == "Сохранить сборку")
def handle_save(message, stop_time):
    with session_factory() as session:
        stmt = insert(Solve).values(user=message.from_user.username, time=stop_time)
        session.execute(stmt)
        session.commit()

        bot.send_message(message.chat.id, f"Сборка успешно сохранена!", reply_markup=repeat_markup)


bot.polling(none_stop=True)
