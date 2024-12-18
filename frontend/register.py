import streamlit as st
import requests

# URL FastAPI сервера
API_URL = "http://127.0.0.1:8000/register"

# Заголовок приложения
st.title("Страница регистрации")

# Поля для ввода
name = email = st.text_input("Имя", placeholder="Введите имя")
email = st.text_input("Почта", placeholder="Введите адрес почты")
username = st.text_input("Имя пользователя", placeholder="Введите имя пользователя")
password = st.text_input("Пароль", placeholder="Введите пароль", type="password")

# Кнопка "Зарегистрироваться"
if st.button("Зарегистрироваться"):
    if username and password:
        # Отправка POST-запроса на сервер FastAPI
        try:
            response = requests.post(API_URL, json={"register_first_name": name, "register_email": email, "register_login": username, "register_password": password})
            if response.status_code == 200:
                st.success("Регистрация успешна!")
            elif response.status_code == 409:
                st.error("Пользователь с таким именем уже существует.")
            else:
                st.error("Произошла ошибка при регистрации.")
        except Exception as e:
            st.error(f"Ошибка подключения к серверу: {e}")
    else:
        st.warning("Пожалуйста, введите имя пользователя и пароль.")