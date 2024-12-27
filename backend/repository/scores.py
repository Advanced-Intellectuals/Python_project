from models import Score, User, Movie
from db import async_session
from sqlalchemy import select, insert
from sqlalchemy.orm import joinedload


class ScoreRepo():
    __async_session = async_session

    async def get_all(self):
        async with self.__async_session() as session:
            statement = select(Score).options(joinedload(
                Score.user), joinedload(Score.movie))
            result = await session.execute(statement)

            scores = result.unique().scalars().all()
            return scores

    async def add_score(self, user_id: int, movie_id: int, score: float) -> bool:
        async with self.__async_session() as session:
            user = await session.get(User, user_id)
            movie = await session.get(Movie, movie_id)

            if not user or not movie:
                return False

            statement = insert(Score).values(
                user_id=user_id, movie_id=movie_id, score=score
            )
            await session.execute(statement)
            await session.commit()

            return True
