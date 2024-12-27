import streamlit as st
from util import draw_movies
import os


def go_to_previous_page():
    if st.session_state.movie_page > 1:
        st.session_state.movie_page -= 1


def go_to_next_page():
    st.session_state.movie_page += 1


def main():
    API_URL = f"{os.getenv('BACK_URL')}/movies"

    movie_grid, params = st.columns([5, 1])

    with params:
        st.write("Дата выхода фильма")
        date1, symb, date2 = st.columns([2, 1, 2], vertical_alignment="bottom")

        with date1:
            number1 = st.number_input("ОТ:", value=1900, step=1)

        with symb:
            st.write("--")

        with date2:
            number2 = st.number_input("ДО:", value=2024, step=1)

        options = ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy', 'Romance', 'Drama',
                   'Action', 'Crime', 'Thriller', 'Horror', 'Mystery', 'Sci-Fi', 'War', 'Musical',
                   'Documentary', 'IMAX', 'Western', 'Film-Noir']

        selected_options = st.multiselect("Жанры:", options)

    if number1 and number2:
        with movie_grid:
            try:
                response = st.session_state.session.get(API_URL, json={"page_number": st.session_state['movie_page'],
                                                                       "start_year": number1,
                                                                       "end_year": number2,
                                                                       "genres": selected_options})
                if response.status_code == 200:
                    body = response.json()
                    draw_movies(body['movies'], 5, __file__)
                else:
                    st.error("Неправильные параметры.")
            except Exception as e:
                st.error(f"Ошибка подключения: {e}")

    page_button_cont1, page_button_cont2 = st.columns(2)
    with page_button_cont1:
        st.button("Предыдущая страница", on_click=go_to_previous_page)
    with page_button_cont2:
        st.button("Следующая страница", on_click=go_to_next_page)
