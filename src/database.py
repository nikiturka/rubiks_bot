import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_PORT = os.environ.get("DB_PORT")
DB_HOST = os.environ.get("DB_HOST")

engine = create_engine(
    url=f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    echo=True
)
session_factory = sessionmaker(engine)


def create_tables():
    with engine.begin() as conn:
        Base.metadata.create_all(engine)
