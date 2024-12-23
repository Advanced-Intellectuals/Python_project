import streamlit as st
import requests

def movie_container(image, text, counter):
    container = st.container()
    with container:
        st.image(image, use_container_width=True)
        if st.button(text, key=counter):
            st.session_state['watching_movie'] = 1
            st.session_state['previous_page'] = 'Личный кабинет'
            st.rerun()

    return container

def draw_movies(movies, columns_per_row):

    for i in range(0, len(movies), columns_per_row):

        cols = st.columns(columns_per_row)
            
        for j, col in enumerate(cols):
            with col:
                movie = movies[i + j] if i + j < len(movies) else None
                if movie:
                    movie_container(movie["image"], movie["text"], i+j)