from fastapi import HTTPException
from repository.users import UserRepo, User
from password_hasher import PasswordHasher


class UserService:
    def __init__(self, user_repo: UserRepo, hasher: PasswordHasher):
        self.user_repo = user_repo
        self.hasher = hasher

    async def login(self, username, password):
        current_user = await self.user_repo.get_by_login(username)

        if current_user is None:
            raise HTTPException(
                status_code=401, detail="A user with this login does not exist.")

        database_password = current_user.password_hash

        if self.hasher.compare(password, database_password):
            return current_user.user_id
        return None

    async def register(self, username, password, first_name, email):
        current_user = await self.user_repo.get_by_login(username)

        if current_user:
            raise HTTPException(
                status_code=409, detail="A user with this username already exists.")
        else:
            user_password = self.hasher.hash(password)
            user = User(login=username, password_hash=user_password,
                        first_name=first_name, email=email)

            await self.user_repo.add(user)
            return user.user_id
