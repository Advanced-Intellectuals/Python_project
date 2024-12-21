from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.responses import PlainTextResponse
from fastapi.responses import JSONResponse
from itsdangerous import URLSafeSerializer, BadSignature
import os
from dotenv import load_dotenv
import requests

from services.user import UserService
from services.movie import MovieService
from models import LoginRequest, RegisterRequest, MainMoviesRequest, UserRequest
from models import SearchMoviesRequest

load_dotenv()


class Serializer():
    def __init__(self):
        self.__serializer = URLSafeSerializer(os.getenv('COOKIE_SECRET_KEY'))

    # Функция для создания сессионной куки
    def create_session(self, user_data: dict):
        session_cookie = self.__serializer.dumps({
            "user_id": user_data["user_id"],
            "role": user_data["role"]
        })
        return session_cookie

    def get_user_data_from_session(self, cookie: str):
        try:
            session_data = self.__serializer.loads(cookie)
            return {
                "user_id": session_data.get("user_id"),
                "role": session_data.get("role")
            }
        except BadSignature:
            return None  # Неверная подпись или кука устарела


class App():
    __app: FastAPI
    __serializer: Serializer

    def __init__(self, user_service: UserService, movie_service: MovieService):
        self.__app = FastAPI()
        self.__serializer = Serializer()

        @self.__app.post("/login")
        async def login(request: Request, response: Response, data: LoginRequest):

            user_login = data.user_login
            user_password = data.user_password

            try:
                user_data = await user_service.login(user_login, user_password)
            except Exception as e:
                raise e

            if user_data:
                # создание сессии
                session_cookie = self.__serializer.create_session(user_data)
                response.set_cookie(
                    key="session",
                    value=session_cookie,
                    httponly=True,  # Защищаем cookie от доступа через JavaScript
                    max_age=3600,  # Время жизни куки (1 час)
                    path='/',  # Путь, для которого действительна кука
                    samesite='Lax'  # Ограничение межсайтовых запросов
                )
            else:
                raise HTTPException(
                    status_code=401, detail="Invalid password.")

        # тестим (или рефакторим или не используем)

        @self.__app.get("/login")
        async def login(request: Request, response: Response):
            session_cookie = request.cookies.get("session")  # Извлекаем куку из запроса
            print(f"Received cookie: {session_cookie}")

            if not session_cookie:
                raise HTTPException(
                    status_code=401, detail="No session cookie found."
                )

            user_data = self.__serializer.get_user_data_from_session(
                session_cookie)  # Извлекаем данные пользователя из куки
            if user_data is None:
                raise HTTPException(
                    status_code=401, detail="Invalid or expired session."
                )

            return {"user_id": user_data["user_id"], "role": user_data["role"]}  # Возвращаем user_id и role в ответе

        @self.__app.post("/register")
        async def register(request: Request, response: Response, data: RegisterRequest):

            user_login = data.register_login
            user_password = data.register_password_hash
            user_first_name = data.register_first_name
            user_email = data.register_email

            try:
                new_user = await user_service.register(user_login, user_password, user_first_name, user_email)
            except Exception as e:
                raise e

            if new_user:
                # создание сессии
                session_cookie = self.__serializer.create_session(new_user)
                response.set_cookie(
                    key="session",
                    value=session_cookie,
                    httponly=True,  # Защищаем cookie от доступа через JavaScript
                    max_age=3600,  # Время жизни куки (1 час)
                    path='/',  # Путь, для которого действительна кука
                    samesite='Lax'  # Ограничение межсайтовых запросов
                )
            else:
                raise HTTPException(
                    status_code=401, detail="Invalid password.")

        @self.__app.get("/recomendations")
        async def reccomendations(request: Request, response: Response):

            session_cookie = request.cookies.get("session")

            if not session_cookie:
                raise HTTPException(status_code=401, detail="No session cookie found.")

            user_data = self.__serializer.get_user_data_from_session(session_cookie)
            if user_data is None:
                raise HTTPException(status_code=401, detail="Invalid or expired session.")

            user_id = user_data["user_id"]
            url = f"http://localhost:8001/recommendations/user/{user_id}"

            try:
                api_response = requests.get(url)
                api_response.raise_for_status()  # Проверяем, что запрос прошёл успешно
                recommendations = api_response.json()  # Извлекаем данные из ответа
                return recommendations  # Возвращаем рекомендации клиенту
            except requests.RequestException as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to fetch recommendations: {str(e)}"
                )

        @self.__app.get("/movies")
        async def main_movies(request: Request, response: Response, data: MainMoviesRequest):

            page_number = data.page_number
            page_size = 15
            start_year = data.start_year
            end_year = data.end_year
            genres = data.genres

            try:
                movies = await movie_service.main_movies(page_number, page_size, start_year, end_year, genres)
            except Exception as e:
                raise e

            return {"movies": movies}

        @self.__app.get("/search")
        async def search(request: Request, response: Response, data: SearchMoviesRequest):

            searched = data.searched_title

            try:
                movies = await movie_service.search_movies(searched)
            except Exception as e:
                raise e

            return {"movies": movies}

        @self.__app.get("/watched")
        async def watched(request: Request, response: Response, data: UserRequest):

            user_id = data.user_id

            try:
                movies = await user_service.watched(user_id)
            except Exception as e:
                raise e

            return {"movies": movies}

        @self.__app.post("/logout")
        async def logout(request: Request, response: Response):
            try:
                # Удаление куки с сессией
                response.delete_cookie(
                    key="session",
                    path='/',  # Должен совпадать с тем, что указан при установке куки
                )
                return {"message": "Successfully logged out"}
            except Exception as e:
                raise HTTPException(status_code=500, detail="Logout failed")

    def get_app(self):
        return self.__app
