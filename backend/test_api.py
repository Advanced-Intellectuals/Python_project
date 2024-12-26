import pytest
from fastapi.testclient import TestClient
from app import App
from services.user import UserService
from services.movie import MovieService
from models import LoginRequest, RegisterRequest, MainMoviesRequest, SearchMoviesRequest, UserRequest

# Mock классы для имитации работы реальных сервисов
class MockUserService:
    async def login(self, user_login, user_password):
        if user_login == "valid_user" and user_password == "valid_pass":
            return {"user_id": 1, "role": "user"}  # Возвращаем ID пользователя
        raise Exception("Invalid credentials")

    async def register(self, user_login, user_password, user_first_name, user_email):
        if user_login == "new_user":
            return {"user_id": 2, "role": "user"}  # Возвращаем ID нового пользователя
        raise Exception("User already exists")

    async def watched(self, user_id):
        if user_id == 1:
            return [{"title": "Watched Movie", "year": 2020}]
        return []

class MockMovieService:
    async def main_movies(self, page_number, page_size, start_year, end_year, genres):
        return [{"title": "Movie 1", "year": 2020}, {"title": "Movie 2", "year": 2021}]

    async def search_movies(self, searched):
        return [{"title": "Searched Movie", "year": 2020}]

# Фикстура для создания клиента тестирования
@pytest.fixture
def client():
    user_service = MockUserService()
    movie_service = MockMovieService()
    app_instance = App(user_service=user_service, movie_service=movie_service)
    return TestClient(app_instance.get_app())

# Тест успешного логина
def test_login_success(client):
    response = client.post(
        "/login",
        json={"user_login": "valid_user", "user_password": "valid_pass"}
    )
    assert response.status_code == 200
    assert "session" in response.cookies

# Тест неудачного логина
def test_login_failure(client):
    response = client.post(
        "/login",
        json={"user_login": "invalid_user", "user_password": "invalid_pass"}
    )
    assert response.status_code == 401

# Тест успешного получения данных из сессии
def test_session_retrieval_success(client):
    # Успешно авторизуемся
    login_response = client.post(
        "/login",
        json={"user_login": "valid_user", "user_password": "valid_pass"}
    )
    assert login_response.status_code == 200
    session_cookie = login_response.cookies.get("session")

    # Проверяем доступ с сессией
    response = client.get("/login", cookies={"session": session_cookie})
    assert response.status_code == 200
    assert response.json() == {"user_id": 1, "role": "user"}

# Тест ошибки при отсутствии или неверной сессии
def test_session_retrieval_failure(client):
    response = client.get("/login", cookies={"session": "invalid_session"})
    assert response.status_code == 401
