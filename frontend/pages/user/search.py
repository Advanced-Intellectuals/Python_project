import streamlit as st
import requests
from util import draw_movies


def main():
    API_URL = "http://127.0.0.1:8000/search"

    search_bar_column, search_button_column = st.columns(
        [4, 1], vertical_alignment="bottom")

    with search_bar_column:
        search_bar = st.text_input("Введите название фильма:")
    if (search_bar):
        try:
            response = requests.get(
                API_URL, json={"searched_title": search_bar})
            if response.status_code == 200:
                body = response.json()
                draw_movies(body['movies'], 6, __file__)
            else:
                st.error("Неправильные параметры.")
        except Exception as e:
            st.error(f"Ошибка подключения: {e}")


if __name__ == "__main__":
    main()
