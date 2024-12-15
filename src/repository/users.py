from sqlalchemy import select
from models import User
from db import async_session


class UserRepo():
    __async_session = async_session

    async def get_all(self):
        async with self.__async_session() as session:
            statement = select(User)

            result = await session.execute(statement)
            return result.scalars()
