from sqlalchemy import select
from models import Movie
from db import async_session


class MovieRepo():
    __async_session = async_session

    async def get_all(self):
        async with self.__async_session() as session:
            statement = select(Movie)

            result = await session.execute(statement)
            return result.scalars()
