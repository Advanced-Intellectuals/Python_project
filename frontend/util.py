import streamlit as st
import requests
import os

DECIPHER_TABLE = {
    "movies": "Главная",
    "recommendations": "Рекомендации",
    "search": "Поиск",
    "watched": "Личный кабинет"
}

def movie_container(image, text, counter, file_path):
    container = st.container()
    with container:
        st.image(image, use_container_width=True)
        if st.button(text, key=counter):
            st.session_state['watching_movie'] = 1
            if file_path in DECIPHER_TABLE:
                st.session_state['previous_page'] = DECIPHER_TABLE[file_path]
            #st.session_state['previous_page'] = DECIPHER_TABLE[file_path]
            #print(file_path, st.session_state['previous_page'])
            st.rerun()

    return container

def draw_movies(movies, columns_per_row, file_path):

    file_path_changed = os.path.splitext(os.path.basename(file_path))[0]

    if (file_path_changed) == 'movie':
        file_path_changed = st.session_state['previous_page']

    for i in range(0, len(movies), columns_per_row):

        cols = st.columns(columns_per_row)
            
        for j, col in enumerate(cols):
            with col:
                movie = movies[i + j] if i + j < len(movies) else None
                if movie:
                    movie_container(movie["image"], movie["text"], i+j, file_path_changed)