import streamlit as st
import requests
from util import draw_movies

movies = [
    {"image": "https://cdn11.bigcommerce.com/s-ydriczk/images/stencil/1500x1500/products/90301/98769/the-creator-original-movie-poster-one-sheet-final-style-buy-now-at-starstills__81077.1697644483.jpg?c=2&imbypass=on", "text": "Movie 1: A thrilling adventure."},
    {"image": "https://cdn11.bigcommerce.com/s-ydriczk/images/stencil/1500x1500/products/90301/98769/the-creator-original-movie-poster-one-sheet-final-style-buy-now-at-starstills__81077.1697644483.jpg?c=2&imbypass=on", "text": "Movie 1: A thrilling adventure."},
    {"image": "https://cdn11.bigcommerce.com/s-ydriczk/images/stencil/1500x1500/products/90301/98769/the-creator-original-movie-poster-one-sheet-final-style-buy-now-at-starstills__81077.1697644483.jpg?c=2&imbypass=on", "text": "Movie 1: A thrilling adventure."},
    {"image": "https://cdn11.bigcommerce.com/s-ydriczk/images/stencil/1500x1500/products/90301/98769/the-creator-original-movie-poster-one-sheet-final-style-buy-now-at-starstills__81077.1697644483.jpg?c=2&imbypass=on", "text": "Movie 1: A thrilling adventure."},
    {"image": "https://cdn11.bigcommerce.com/s-ydriczk/images/stencil/1500x1500/products/90301/98769/the-creator-original-movie-poster-one-sheet-final-style-buy-now-at-starstills__81077.1697644483.jpg?c=2&imbypass=on", "text": "Movie 1: A thrilling adventure."},
    {"image": "https://cdn11.bigcommerce.com/s-ydriczk/images/stencil/1500x1500/products/90301/98769/the-creator-original-movie-poster-one-sheet-final-style-buy-now-at-starstills__81077.1697644483.jpg?c=2&imbypass=on", "text": "Movie 1: A thrilling adventure."},
    {"image": "https://cdn11.bigcommerce.com/s-ydriczk/images/stencil/1500x1500/products/90301/98769/the-creator-original-movie-poster-one-sheet-final-style-buy-now-at-starstills__81077.1697644483.jpg?c=2&imbypass=on", "text": "Movie 1: A thrilling adventure."},
    {"image": "https://cdn11.bigcommerce.com/s-ydriczk/images/stencil/1500x1500/products/90301/98769/the-creator-original-movie-poster-one-sheet-final-style-buy-now-at-starstills__81077.1697644483.jpg?c=2&imbypass=on", "text": "Movie 1: A thrilling adventure."}
]

def main():
    API_URL = "http://127.0.0.1:8000/movies"

    movie_grid, params = st.columns([6, 1])

    with movie_grid:
        draw_movies(movies, 6, __file__)

    with params:
        st.write("Дата выхода фильма")
        date1, symb, date2 = st.columns([2,1,2], vertical_alignment="bottom")

        with date1:
            number1 = st.number_input("ОТ:", value=1980, step=1)

        with symb:
            st.write("--")

        with date2:
            number2 = st.number_input("ДО:", value=2024, step=1)

        options = ["Option 1", "Option 2", "Option 3"]
        selected_options = st.multiselect("Жанры:", options)
        if st.button("Применить"):
            if selected_options and date1 and date2:
                st.write("Будет применён фильтр")
            else:
                st.warning("Сначала заполните поля!")


    page_button_cont1, page_button_cont2 = st.columns(2)
    with page_button_cont1:
        if st.button("Предыдущая страница"):
            st.write("Переход назад")
    with page_button_cont2:
        if st.button("Следующая страница"):
            st.write("Переход вперёд")

if __name__ == "__main__":
    main()