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
    API_URL = "http://127.0.0.1:8000/watched"

    _, exit_button_column = st.columns([8,1], vertical_alignment="top")
    
    with exit_button_column:
        exit_button = st.button("Выйти из аккаунта")
    if exit_button:
        st.session_state['logged'] = 0
        st.rerun()
    
    st.title("Просмотренные фильмы:")

    draw_movies(movies, 6, __file__)

if __name__ == "__main__":
    main()