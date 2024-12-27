import streamlit as st
import os
from util import draw_movies


def main():
    API_URL_WATCHED = f"{os.getenv('BACK_URL')}/watched"
    API_URL_LOGOUT = f"{os.getenv('BACK_URL')}/logout"

    _, exit_button_column = st.columns([8, 1], vertical_alignment="top")

    with exit_button_column:
        exit_button = st.button("Выйти из аккаунта")
    if exit_button:
        try:
            response = st.session_state.session.post(API_URL_LOGOUT)
            if response.status_code == 200:
                st.session_state['logged'] = 0
                st.rerun()
            else:
                st.error("Неправильные параметры.")
        except Exception as e:
            st.error(f"Ошибка подключения: {e}")

    st.title("Просмотренные фильмы:")
    try:
        response = st.session_state.session.get(API_URL_WATCHED)
        if response.status_code == 200:
            body = response.json()
            draw_movies(body['movies'], 6, __file__)
        else:
            st.error("Неправильные параметры.")
    except Exception as e:
        st.error(f"Ошибка подключения: {e}")
