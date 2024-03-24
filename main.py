import time
from telebot import types
import telebot
from sqlalchemy import select, insert
from markups import stop_markup, start_markup, save_markup, repeat_markup
from services.scramble_service import ScrambleService
from src.database import create_tables, session_factory
from src.models import User, Solve

bot = telebot.TeleBot("6745385275:AAESHGHgt1wF1zBXtbQPvcJoNAaUQ79TXjU")
solve = {}
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
    generated_scramble = ScrambleService.generate_scramble()

    bot.send_message(
        message.chat.id,
        f"Ваш скрамбл - {generated_scramble}\nHажмите 'Старт' для запуска секундомера",
        reply_markup=start_markup
    )

    solve["scramble"] = generated_scramble
    solve["user"] = message.from_user.username


@bot.message_handler(func=lambda message: message.text == "Старт")
def handle_start(message):
    start_time = time.time()
    bot.send_message(message.chat.id, "Таймер запущен!", reply_markup=stop_markup)
    bot.register_next_step_handler(message, lambda msg: handle_stop(msg, start_time))


@bot.message_handler(func=lambda message: message.text == "Стоп")
def handle_stop(message, s_time):
    stop_time = time.time() - s_time
    solve["time"] = f"{stop_time:.2f}"

    bot.send_message(message.chat.id, f"Ваше время: {stop_time:.2f} секунд.", reply_markup=save_markup)


@bot.message_handler(func=lambda message: message.text == "Пропустить сборку")
def handle_skip(message):
    solve.clear()

    bot.send_message(message.chat.id, f"Сборка не была сохранена.", reply_markup=repeat_markup)


@bot.message_handler(func=lambda message: message.text == "Сохранить сборку")
def handle_save(message):
    with session_factory() as session:
        stmt = insert(Solve).values(**solve)
        session.execute(stmt)
        session.commit()

        solve.clear()

        bot.send_message(message.chat.id, f"Сборка успешно сохранена!", reply_markup=repeat_markup)


@bot.message_handler(func=lambda message: message.text == "Следующая сборка")
def repeat_solve(message):
    scramble(message)


@bot.message_handler(func=lambda message: message.text == "Выход")
def exit_solves(message):
    bot.send_message(message.chat.id, f"Ладно-ладно :-(", reply_markup=types.ReplyKeyboardRemove())


bot.polling(none_stop=True)
