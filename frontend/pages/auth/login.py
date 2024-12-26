import streamlit as st
import requests

def main():
    API_URL = "http://127.0.0.1:8000/login"

    st.title("Авторизация")

    username = st.text_input("Логин", placeholder="Введите логин")
    password = st.text_input("Пароль", placeholder="Введите пароль", type="password")

    if st.button("Войти"):
        if username and password:
            try:
                response = requests.post(API_URL, json={"user_login": username, "user_password": password})
                if response.status_code == 200:
                    st.success("Вы совершили вход!")
                    st.session_state['logged'] = 1
                    st.rerun()
                else:
                    st.error("Неправильный логин или пароль.")
            except Exception as e:
                st.error(f"Ошибка подключения: {e}")
        else:
            st.warning("Пожалуйста введите логин и пароль.")
    
    if st.button("Ещё нет аккаунта?"):
        st.session_state['auth_page'] = 'register'
        st.rerun()

if __name__ == "__main__":
    main()