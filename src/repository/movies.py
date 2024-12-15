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
            return movies
