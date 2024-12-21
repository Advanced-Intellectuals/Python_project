from sqlalchemy import select, insert
from sqlalchemy.orm import joinedload
from src.models import Score, User, watched_table
from src.db import async_session


class Repository:
    __async_session = async_session

    async def get_all(self):
        async with self.__async_session() as session:
            statement = select(Score)

            res = await session.execute(statement)
            scores = res.scalars().all()

            return [[s.user_id, s.movie_id, s.score] for s in scores]

    async def get_watched(self, user_id: int):
        async with self.__async_session() as session:
            statement = select(User).options(joinedload(
                User.watched_movies), joinedload(User.scores)).where(User.user_id == user_id)

            res = await session.execute(statement)
            watched = res.scalars().first().watched_movies

            return [w.movie_id for w in watched]
