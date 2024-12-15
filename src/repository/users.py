from sqlalchemy import select
from sqlalchemy.orm import joinedload
from models import User
from db import async_session


class UserRepo():
    __async_session = async_session

    async def get_all(self):
        async with self.__async_session() as session:
            statement = select(User).options(joinedload(
                User.watched_movies), joinedload(User.scores)).order_by(User.user_id)
            result = await session.execute(statement)

            users = result.unique().scalars().all()
            return users
