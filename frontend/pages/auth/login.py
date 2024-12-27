import streamlit as st
import os


def login():
    if st.session_state.username and st.session_state.password:
        try:
            response = st.session_state.session.post(
                st.session_state.api_url,
                json={"user_login": st.session_state.username,
                      "user_password": st.session_state.password}
            )
            if response.status_code == 200:
                response2 = st.session_state.session.get(
                    st.session_state.api_url)
                if response2.status_code == 200:
                    body = response2.json()
                    if body['role'] == 'user':
                        st.session_state['logged'] = 1
                    elif body['role'] == 'admin':
                        st.session_state['logged'] = 2
                else:
                    st.error("Не удалось получить роль")
            else:
                st.error("Неправильный логин или пароль.")
        except Exception as e:
            st.error(f"Ошибка подключения: {e}")
    else:
        st.warning("Пожалуйста введите логин и пароль.")


def reg():
    st.session_state['auth_page'] = 'register'


def main():
    API_URL = f"{os.getenv('BACK_URL')}/login"

    st.title("Авторизация")

    st.session_state.username = st.text_input(
        "Логин", placeholder="Введите логин")
    st.session_state.password = st.text_input(
        "Пароль", placeholder="Введите пароль", type="password")

    st.button("Войти", on_click=login)

    st.button("Ещё нет аккаунта?", on_click=reg)
