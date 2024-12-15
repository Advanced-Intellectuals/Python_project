from models import Score
from db import async_session
from sqlalchemy import select


class ScoreRepo():
    __async_session = async_session

    async def get_all(self):
        async with self.__async_session() as session:
            statement = select(Score)

            result = await session.execute(statement)
            return result.scalars()
