from app import App
from services.user import UserService
from repository.users import UserRepo
from password_hasher import PasswordHasher


class CompositionRoot():
    def __init__(self):
        hasher = PasswordHasher()

        user_repo = UserRepo()

        user_service = UserService(user_repo, hasher)

        self.__app = App(user_service)

    def get_app(self):
        return self.__app.get_app()
