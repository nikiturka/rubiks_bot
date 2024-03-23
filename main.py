import time
import telebot
from sqlalchemy import select, insert
from markups import stop_markup, start_markup
from src.database import create_tables, session_factory
from src.models import User

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
    bot.send_message(message.chat.id, f"Ваше время: {stop_time:.2f} секунд.")


bot.polling(none_stop=True)
