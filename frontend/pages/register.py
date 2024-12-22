import streamlit as st
import requests

def main():
    API_URL = "http://127.0.0.1:8000/register"

    st.title("Регистрация")

    name = email = st.text_input("Имя", placeholder="Введите имя")
    email = st.text_input("Почта", placeholder="Введите адрес почты")
    username = st.text_input("Имя пользователя", placeholder="Введите имя пользователя")
    password = st.text_input("Пароль", placeholder="Введите пароль", type="password")

    if st.button("Зарегистрироваться"):
        if username and password:
            try:
                response = requests.post(API_URL, json={"register_first_name": name, "register_email": email, "register_login": username, "register_password": password})
                if response.status_code == 200:
                    st.success("Регистрация успешна!")
                    st.session_state['logged'] = 1
                    st.rerun()
                elif response.status_code == 409:
                    st.error("Пользователь с таким именем уже существует.")
                else:
                    st.error("Произошла ошибка при регистрации.")
            except Exception as e:
                st.error(f"Ошибка подключения к серверу: {e}")
        else:
            st.warning("Пожалуйста, введите имя пользователя и пароль.")
    
    if st.button("Уже есть аккаунт?"):
        st.session_state['auth_page'] = 'login'
        st.rerun()

if __name__ == "__main__":
    main()