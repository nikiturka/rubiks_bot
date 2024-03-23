import datetime
from typing import Annotated

from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    username: Mapped[str]


class Solve(Base):
    __tablename__ = 'solves'

    id: Mapped[intpk]
    time: Mapped[float]
    user: Mapped[str]
    created_at: Mapped[created_at]
    scramble: Mapped[str] = mapped_column(nullable=True)
