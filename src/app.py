from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.responses import PlainTextResponse
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from itsdangerous import URLSafeSerializer, BadSignature
import os

from services.login import UserService
from password_hasher import PasswordHasher
from repository.users import UserRepo

app = FastAPI()

SECRET_KEY = "your_secret_key"
serializer = URLSafeSerializer(SECRET_KEY)

class LoginRequest(BaseModel):
    user_login: str
    user_password: str

# Функция для создания сессионной куки
def create_session(user_id: int):
    session_cookie = serializer.dumps({"user_id": user_id})
    return session_cookie

# Функция для извлечения user_id из сессионной куки
def get_user_id_from_session(cookie: str):
    try:
        session_data = serializer.loads(cookie)
        return session_data.get("user_id")
    except BadSignature:
        return None  # Неверная подпись или кука устарела

@app.post("/login")
async def login(request: Request, response: Response, data: LoginRequest):
    user_login = data.user_login
    user_password = data.user_password

    user_repo = UserRepo()
    hasher = PasswordHasher()

    service = UserService(user_repo, hasher)
    try:
        user_id = await service.login(user_login, user_password)
    except Exception as e:
        raise e

    if user_id:
        # создание сессии
        session_cookie = create_session(user_id)
        response.set_cookie(
            key="session",
            value=session_cookie,
            httponly=True,  # Защищаем cookie от доступа через JavaScript
            max_age=3600,  # Время жизни куки (1 час)
            path='/',  # Путь, для которого действительна кука
            samesite='Lax'  # Ограничение межсайтовых запросов
        )
    else:
        raise HTTPException(status_code=401, detail="Invalid password.")

# тестим (или рефакторим или не используем)
@app.get("/login")
async def login(request: Request, response: Response):
    session_cookie = request.cookies.get("session")  # Извлекаем куку из запроса
    print(f"Received cookie: {session_cookie}")
    if not session_cookie:
        raise HTTPException(status_code=401, detail="No session cookie found.")

    user_id = get_user_id_from_session(session_cookie)  # Извлекаем user_id из куки
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid or expired session.")

    return {"user_id": user_id}  # Возвращаем user_id в ответе

@app.get("/register")
def register():
    user_login = "user1"    # типа получили данные от Максима
    user_password = "pass1"
    user_first_name = "Толя"
    user_mail = "user1@mail.ru"