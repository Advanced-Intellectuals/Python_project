from db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import select, ARRAY, String, Integer


class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    login: Mapped[str] = mapped_column(Integer, nullable=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, nullable=True)

    def __repr__(self) -> str:
        return f"<User {self.user_id} {self.login} {self.password_hash} {self.first_name} {self.email}>"


class Movie(Base):
    __tablename__ = 'movies'

    movie_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    genres: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)

    def __repr__(self) -> str:
        return f"<Movie {self.movie_id} {self.name} {self.genres} {self.year}>"
