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

    async def get_by_login(self, login: str):
        async with self.__async_session() as session:
            statement = select(User).options(
                joinedload(User.watched_movies),
                joinedload(User.scores)).where(User.login == login)
            result = await session.execute(statement)

            user = result.scalars().first()
            return user

    async def write(self, user: User):
        async with self.__async_session() as session:
            session.add(user)
            await session.commit()
