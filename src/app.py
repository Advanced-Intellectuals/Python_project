from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.responses import PlainTextResponse
from fastapi.responses import JSONResponse
from itsdangerous import URLSafeSerializer, BadSignature
import os
from dotenv import load_dotenv

from services.user import UserService
from models import LoginRequest, RegisterRequest


load_dotenv


class Serializer():
    def __init__(self):
        self.__serializer = URLSafeSerializer(os.getenv('COOKIE_SECRET_KEY'))

    # Функция для создания сессионной куки
    def create_session(self, user_id: int):
        session_cookie = self.__serializer.dumps({"user_id": user_id})
        return session_cookie

    # Функция для извлечения user_id из сессионной куки
    def get_user_id_from_session(self, cookie: str):
        try:
            session_data = self.__serializer.loads(cookie)
            return session_data.get("user_id")
        except BadSignature:
            return None  # Неверная подпись или кука устарела


class App():
    __app: FastAPI
    __serializer: Serializer

    def __init__(self, user_service: UserService):
        __app = FastAPI()
        __serializer = Serializer()

        @__app.post("/login")
        async def login(request: Request, response: Response, data: LoginRequest):
            user_login = data.user_login
            user_password = data.user_password

            try:
                user_id = await user_service.login(user_login, user_password)
            except Exception as e:
                raise e

            if user_id:
                # создание сессии
                session_cookie = __serializer.create_session(user_id)
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

        @__app.get("/login")
        async def login(request: Request, response: Response):
            session_cookie = request.cookies.get(
                "session")  # Извлекаем куку из запроса
            print(f"Received cookie: {session_cookie}")
            if not session_cookie:
                raise HTTPException(
                    status_code=401, detail="No session cookie found.")

            user_id = __serializer.get_user_id_from_session(
                session_cookie)  # Извлекаем user_id из куки
            if user_id is None:
                raise HTTPException(
                    status_code=401, detail="Invalid or expired session.")

            return {"user_id": user_id}  # Возвращаем user_id в ответе

        @__app.post("/register")
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
                session_cookie = __serializer.create_session(new_user)
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

    def get_app(self):
        return self.__app
