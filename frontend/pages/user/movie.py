import streamlit as st
import requests
from util import draw_movies
import os


def movie(movie_id):
    API_URL_MOVIE = f"{os.getenv('BACK_URL')}/movies/{movie_id}"
    API_URL_SCORE = f"{os.getenv('BACK_URL')}/add_score"
    API_URL_RECS = f"{os.getenv('BACK_URL')}/similar_movies"

    if st.button("К фильмам"):
        st.session_state['watching_movie'] = 0
        st.rerun()

    movie_info, video = st.columns([1, 3])
    with movie_info:
        try:
            response = st.session_state.session.get(API_URL_MOVIE)
            if response.status_code == 200:
                movie = response.json()
                st.image(st.session_state.minio_server.get_object_url(
                    movie["preview"]), use_container_width=True)
                st.write(movie["name"])
                st.write(movie["year"])
                st.write(", ".join(map(str, movie["genres"])))
            else:
                st.error("Ошибка запроса.")
        except Exception as e:
            st.error(f"Ошибка подключения: {e}")
    with video:
        st.video(st.session_state.minio_server.get_object_url(
            movie["file"]))
    selecter, _ = st.columns([1, 5])
    with selecter:
        selected_value = st.selectbox('Поставьте оценку:', range(1, 11))
        if (st.button('Поставить')):
            try:
                response = st.session_state.session.post(
                    API_URL_SCORE, json={"movie_id": movie_id, "score": selected_value})
                if response.status_code == 201:
                    st.success("Оценка поставлена!")
                else:
                    st.error("Ошибка запроса.")
            except Exception as e:
                st.error(f"Ошибка подключения: {e}")

    st.title('Также смотрят:')

    try:
        response = st.session_state.session.get(
            API_URL_RECS, json={'movie_id': movie_id})
        if response.status_code == 200:
            body = response.json()
            draw_movies(body, 5, __file__)
        else:
            st.error("Ошибка запроса.")
            st.error(response.json())
    except Exception as e:
        st.error(f"Ошибка подключения: {e}")
