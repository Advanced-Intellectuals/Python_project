import streamlit as st
import requests

def movie_container(image, text, width="200 px"):
    container = st.container()
    with container:
        st.image(image, use_container_width=True)
        st.markdown(f"<p style='text-align: center;'>{text}</p>", unsafe_allow_html=True)

    return container

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
    API_URL = "http://127.0.0.1:8000/movies"

    movie_grid, params = st.columns([6, 1])

    with movie_grid:
        columns_per_row = 6

        for i in range(0, len(movies), columns_per_row):

            cols = st.columns(columns_per_row)
            
            for j, col in enumerate(cols):
                with col:
                    movie = movies[i + j] if i + j < len(movies) else None
                    if movie:
                        movie_container(movie["image"], movie["text"])
    with params:
        st.write("Дата выхода:")
        date1, symb, date2 = st.columns([2,1,2], vertical_alignment="bottom")

        with date1:
            number1 = st.number_input("", value=1980, step=1)

        with symb:
            st.write("--")

        with date2:
            number2 = st.number_input("", value=2024, step=1)

        options = ["Option 1", "Option 2", "Option 3"]
        selected_options = st.multiselect("Жанры:", options)


    st.title("Тут будут фильмы")

if __name__ == "__main__":
    main()