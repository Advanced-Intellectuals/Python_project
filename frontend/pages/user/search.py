import streamlit as st
import os
from util import draw_movies


def find():
    if (st.session_state.search_bar):
        try:
            response = st.session_state.session.get(
                st.session_state.search_url, json={"searched_title": st.session_state.search_bar})
            if response.status_code == 200:
                body = response.json()
                draw_movies(body['movies'], 6, __file__)
            else:
                st.error("Неправильные параметры.")
        except Exception as e:
            st.error(f"Ошибка подключения: {e}")


def main():
    st.session_state.search_url = f"{os.getenv('BACK_URL')}/search"

    search_bar_column, search_button_column = st.columns(
        [4, 1], vertical_alignment="bottom")

    with search_bar_column:
        st.session_state.search_bar = st.text_input("Введите название фильма:")
    with search_button_column:
        st.button('Найти', on_click=find)
