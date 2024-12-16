from sqlalchemy import select
from sqlalchemy.orm import joinedload
from models import Movie
from db import async_session


class MovieRepo():
    __async_session = async_session

    async def get_all(self):
        async with self.__async_session() as session:
            statement = select(Movie).options(joinedload(
                Movie.watched_by), joinedload(Movie.scores)).order_by(Movie.movie_id)
            result = await session.execute(statement)

            movies = result.unique().scalars().all()

            for m in movies:
                m.preview = str(m.preview)
                m.file = str(m.file)
            return movies

    async def get_by_id(self, id: int):
        async with self.__async_session() as session:
            statement = select(Movie).options(joinedload(
                Movie.watched_by), joinedload(Movie.scores)).where(Movie.movie_id == id)

            result = await session.execute(statement)

            movie = result.scalars().first()
            movie.preview = str(movie.preview)
            movie.file = str(movie.file)

            return movie

    async def write(self, movie: Movie):
        async with self.__async_session() as session:
            session.add(movie)
            await session.commit()

    async def delete(self, id: int):
        async with self.__async_session() as session:
            statement = select(Movie).options(joinedload(
                Movie.watched_by), joinedload(Movie.scores)).where(Movie.movie_id == id)

            result = await session.execute(statement)

            movie = result.scalars().first()
            await session.delete(movie)

            await session.commit()
