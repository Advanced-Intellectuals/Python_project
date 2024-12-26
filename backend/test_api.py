import pytest
from fastapi.testclient import TestClient
from app import App
from services.user import UserService
from services.movie import MovieService
from models import LoginRequest, RegisterRequest, MainMoviesRequest, SearchMoviesRequest, UserRequest
from pytest_mock import MockerFixture, mocker
import requests


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


class MockMovieService:
    async def main_movies(self, page_number, page_size, start_year, end_year, genres):
        return [{"title": "Movie 1", "year": 2020}, {"title": "Movie 2", "year": 2021}]

    async def search_movies(self, searched):
        return [{"title": "Searched Movie", "year": 2020}]

    async def recommend_movies(self, recommendations):
        if recommendations == [1, 2, 3]:
            return [
                {"id": 1, "title": "Recommended Movie 1"},
                {"id": 2, "title": "Recommended Movie 2"},
                {"id": 3, "title": "Recommended Movie 3"}
            ]
        return []


class MockScoreService:
    async def calculate_score(self, user_id, movie_id):
        return {"movie_id": movie_id, "score": 4.5}


# Фикстура для создания клиента тестирования
@pytest.fixture
def client_local():
    user_service = MockUserService()
    movie_service = MockMovieService()
    score_service = MockScoreService()
    app_instance = App(user_service=user_service, movie_service=movie_service, score_service=score_service)
    return TestClient(app_instance.get_app())

@pytest.fixture
def client_global(mocker):
    user_service = MockUserService()
    movie_service = MockMovieService()
    score_service = MockScoreService()
    app_instance = App(user_service=user_service, movie_service=movie_service, score_service=score_service)

    # Мокаем внешний вызов API
    mocker.patch(
        "requests.get",
        return_value=mocker.Mock(status_code=200, json=lambda: {"recommendations": [1, 2, 3]})
    )

    return TestClient(app_instance.get_app())

@pytest.fixture
def client_global_on_my_api():
    user_service = MockUserService()
    movie_service = MockMovieService()
    score_service = MockScoreService()
    app_instance = App(user_service=user_service, movie_service=movie_service, score_service=score_service)

    return TestClient(app_instance.get_app())

# Тест успешного логина
def test_login_success(client_local):
    response = client_local.post(
        "/login",
        json={"user_login": "valid_user", "user_password": "valid_pass"}
    )
    assert response.status_code == 200
    assert "session" in response.cookies

# Тест неудачного логина
def test_login_failure(client_local):
    response = client_local.post(
        "/login",
        json={"user_login": "invalid_user", "user_password": "invalid_pass"}
    )
    assert response.status_code == 401

# Тест успешного получения данных из сессии
def test_session_retrieval_success(client_local):
    # Успешно авторизуемся
    login_response = client_local.post(
        "/login",
        json={"user_login": "valid_user", "user_password": "valid_pass"}
    )
    assert login_response.status_code == 200
    session_cookie = login_response.cookies.get("session")

    # Проверяем доступ с сессией
    response = client_local.get("/login", cookies={"session": session_cookie})
    assert response.status_code == 200
    assert response.json() == {"user_id": 1, "role": "user"}

# Тест ошибки при отсутствии или неверной сессии
def test_session_retrieval_failure(client_local):
    response = client_local.get("/login", cookies={"session": "invalid_session"})
    assert response.status_code == 401

# Тест успешной регистрации
def test_register_cookie_set(client_local):
    response = client_local.post(
        "/register",
        json={
            "register_login": "new_user",
            "register_password_hash": "secure_password",
            "register_first_name": "John",
            "register_email": "john.doe@example.com"
        }
    )
    assert response.status_code == 200
    assert "session" in response.cookies

# Тест неудачной регистрации
def test_register_cookie_not_set(client_local):
    response = client_local.post(
        "/register",
        json={
            "register_login": "existing_user",
            "register_password_hash": "some_password",
            "register_first_name": "Jane",
            "register_email": "jane.doe@example.com"
        }
    )
    assert response.status_code == 417
    assert "session" not in response.cookies

def test_recommendations_with_valid_session(client_global):
    # Успешно авторизуемся
    response = client_global.post(
        "/login",
        json={"user_login": "valid_user", "user_password": "valid_pass"}
    )
    assert response.status_code == 200
    session_cookie = response.cookies.get("session")

    # Запрашиваем рекомендации
    recommendations_response = client_global.get(
        "/recommendations",
        cookies={"session": session_cookie}
    )
    assert recommendations_response.status_code == 200
    assert recommendations_response.json() == [
        {"id": 1, "title": "Recommended Movie 1"},
        {"id": 2, "title": "Recommended Movie 2"},
        {"id": 3, "title": "Recommended Movie 3"}
    ]

def test_recommendations_without_session(client_global):
    response = client_global.get("/recommendations")
    assert response.status_code == 401
    assert response.json() == {"detail": "No session cookie found."}

