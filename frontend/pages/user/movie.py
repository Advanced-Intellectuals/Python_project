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
    API_URL = "http://127.0.0.1:8000/movie"

    if st.button("К фильмам"):
        st.session_state['watching_movie'] = 0
        st.rerun()
    
    movie_info, video = st.columns([1,3])
    with movie_info:
        st.image('https://cdn11.bigcommerce.com/s-ydriczk/images/stencil/1500x1500/products/90301/98769/the-creator-original-movie-poster-one-sheet-final-style-buy-now-at-starstills__81077.1697644483.jpg?c=2&imbypass=on')
        st.write('Название')
        st.write('Год')
        genres = ['А','Б','В']
        st.write(", ".join(map(str, genres)))
    with video:
        st.video('https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DknRAM6AHcKI&psig=AOvVaw3_dWJFpuI3mYjZzu6xCUlp&ust=1735054361132000&source=images&cd=vfe&opi=89978449&ved=0CBcQjhxqFwoTCKDnlqmbvooDFQAAAAAdAAAAABAE')
    selecter, _ = st.columns([1,5])
    with selecter:
        selected_value = st.selectbox('Поставьте оценку:', range(1, 11),)
    st.write('Ваша оценка: ', selected_value)
    st.title('Также смотрят:')
    draw_movies(movies, 5, __file__)

if __name__ == "__main__":
    main()