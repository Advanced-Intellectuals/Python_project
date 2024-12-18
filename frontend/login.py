import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/login"

st.title("Авторизация")

username = st.text_input("Логин", placeholder="Введите логин")
password = st.text_input("Пароль", placeholder="Введите пароль", type="password")

if st.button("Login"):
    if username and password:
        try:
            response = requests.post(API_URL, json={"login": username, "password": password})
            if response.status_code == 200:
                st.success("Вы совершили вход!")
            else:
                st.error("Неправильный логин или пароль.")
        except Exception as e:
            st.error(f"Ошибка подключения: {e}")
    else:
        st.warning("Пожалуйста введите логин и пароль.")