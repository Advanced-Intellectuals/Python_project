from app import App
from services.user import UserService
from services.movie import MovieService
from services.score import ScoreService
from repository.users import UserRepo
from repository.movies import MovieRepo
from repository.scores import ScoreRepo
from password_hasher import PasswordHasher


class CompositionRoot():
    def __init__(self):
        hasher = PasswordHasher()

        user_repo = UserRepo()

        user_service = UserService(user_repo, hasher)

        movie_repo = MovieRepo()

        movie_service = MovieService(movie_repo)

        score_repo = ScoreRepo()

        score_service = ScoreService(score_repo)

        self.__app = App(user_service, movie_service, score_service)

    def get_app(self):
        return self.__app.get_app()
