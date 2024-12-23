import streamlit as st
import requests
from util import draw_movies

# Example data: images and texts for movies
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
    API_URL = "http://127.0.0.1:8000/search"

    search_bar_column, search_button_column = st.columns([4,1], vertical_alignment="bottom")
    
    with search_bar_column:
        search_bar = st.text_input("Введите название фильма:")
    with search_button_column:
        search_button = st.button("Искать")

    if search_button:
        if search_bar:

            draw_movies(movies, 6)
            
        else:
            st.warning("Введите название!")

if __name__ == "__main__":
    main()