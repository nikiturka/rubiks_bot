import telebot
from sqlalchemy import select, insert
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


bot.polling(none_stop=True)
