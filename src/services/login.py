from fastapi import FastAPI, HTTPException, Depends, Request, Response
from repository.users import UserRepo, User
from password_hasher import PasswordHasher

class UserService:
    def __init__(self, user_repo, hasher):
        self.user_repo = user_repo
        self.hasher = hasher

    async def login(self, username, password):
        current_user = await self.user_repo.get_by_login(username)

        if current_user is None: raise HTTPException(status_code=401, detail="A user with this login does not exist.")

        database_password = current_user.password_hash

        if self.hasher.compare(password, database_password):
            return current_user.user_id
        return None
