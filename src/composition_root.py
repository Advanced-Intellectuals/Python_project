from app import App
from services.user import UserService
from services.movie import MovieService
from repository.users import UserRepo
from repository.movies import MovieRepo
from password_hasher import PasswordHasher


class CompositionRoot():
    def __init__(self):
        hasher = PasswordHasher()

        user_repo = UserRepo()

        user_service = UserService(user_repo, hasher)

        movie_repo = MovieRepo()

        movie_service = MovieService(movie_repo)

        self.__app = App(user_service, movie_service)

    def get_app(self):
        return self.__app.get_app()
