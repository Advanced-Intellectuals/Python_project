from db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, BigInteger, ForeignKey, Column, Table, Double
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from pydantic import BaseModel
from typing import Optional

watched_table = Table(
    'watched',
    Base.metadata,
    Column(
        'user_id',
        BigInteger,
        ForeignKey('users.user_id', ondelete='CASCADE'),
        primary_key=True
    ),

    Column(
        'movie_id',
        BigInteger,
        ForeignKey('movies.movie_id', ondelete='CASCADE'),
        primary_key=True
    )
)


class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    login: Mapped[str] = mapped_column(String, nullable=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=True)
    role: Mapped[str] = mapped_column(String, nullable=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, nullable=True)

    scores = relationship(
        'Score', back_populates='user',
        cascade='all, delete-orphan'
    )

    watched_movies = relationship(
        'Movie',
        secondary=watched_table,
        back_populates='watched_by'
    )

    def __repr__(self) -> str:
        return f"<User {self.user_id} {self.login} {self.password_hash} {self.first_name} {self.email}>"


class Movie(Base):
    __tablename__ = 'movies'

    movie_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    genres: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    year: Mapped[int] = mapped_column(BigInteger, nullable=False)
    preview: Mapped[str] = mapped_column(UUID(as_uuid=True), nullable=False)
    file: Mapped[str] = mapped_column(UUID(as_uuid=True), nullable=False)

    scores = relationship(
        'Score', back_populates='movie',
        cascade='all, delete-orphan'
    )

    watched_by = relationship(
        'User',
        secondary=watched_table,
        back_populates='watched_movies'
    )

    def __repr__(self) -> str:
        return f"<Movie {self.movie_id} {self.name} {self.genres} {self.year}>"


class Score(Base):
    __tablename__ = 'scores'

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey('users.user_id'),
        nullable=False,
        primary_key=True
    )

    movie_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('movies.movie_id'),
        nullable=False,
        primary_key=True
    )

    score: Mapped[float] = mapped_column(Double, nullable=False)

    user = relationship('User', back_populates='scores')
    movie = relationship('Movie', back_populates='scores')

    def __repr__(self) -> str:
        return f"<Score {self.user_id} {self.movie_id} {self.score}>"


class LoginRequest(BaseModel):
    user_login: str
    user_password: str


class RegisterRequest(BaseModel):
    register_login: str
    register_password_hash: str
    register_first_name: str
    register_email: str

class MainMoviesRequest(BaseModel):
    page_number: int
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    genres: Optional[list[str]] = None

class SearchMoviesRequest(BaseModel):
    searched_title: str

class AddMovieRequest(BaseModel):
    name: str
    genres: list[str]
    year: int
    preview: str
    file: str

class UserRequest(BaseModel):
    user_id: int

class MovieRequest(BaseModel):
    movie_id: int