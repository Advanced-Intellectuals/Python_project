from sqlalchemy import select, insert
from sqlalchemy.orm import joinedload
from models import User, Movie, watched_table
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

    async def add(self, user: User):
        async with self.__async_session() as session:
            session.add(user)
            await session.commit()

    async def delete(self, login: User):
        async with self.__async_session() as session:
            statement = select(User).options(
                joinedload(User.watched_movies),
                joinedload(User.scores)).where(User.login == login)
            result = await session.execute(statement)

            user = result.scalars().first()
            await session.delete(user)

            await session.commit()

    async def add_watched(self, user_id: int, movie_id: int) -> bool:
        async with self.__async_session() as session:
            user = await session.get(User, user_id)
            movie = await session.get(Movie, movie_id)

            if not user or not movie:
                return False

            statement = insert(watched_table).values(
                user_id=user_id, movie_id=movie_id)
            await session.execute(statement)
            await session.commit()

            return True
