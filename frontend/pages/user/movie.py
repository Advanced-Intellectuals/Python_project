import streamlit as st
import requests
from util import draw_movies
import minio_server

def movie(movie_id):
    API_URL_MOVIE = f"http://127.0.0.1:8000/movie/{movie_id}"
    API_URL_RECS = f"http://127.0.0.1:8000/similar_movies"

    if st.button("К фильмам"):
        st.session_state['watching_movie'] = 0
        st.rerun()
    
    movie_info, video = st.columns([1,3])
    with movie_info:
        try:
            response = requests.get(API_URL_MOVIE)
            if response.status_code == 200:
                st.image(st.image(minio_server.MinioServer().get_object_url(movie["preview"]), use_container_width=True))
                st.write(movie["name"])
                st.write(movie["year"])
                st.write(movie["year"])
                st.write(", ".join(map(str, movie["genres"])))
            else:
                st.error("Ошибка запроса.")
        except Exception as e:
            st.error(f"Ошибка подключения: {e}")
    with video:
        st.video(st.image(minio_server.MinioServer().get_object_url(movie["preview"]), use_container_width=True))
    selecter, _ = st.columns([1,5])
    with selecter:
        selected_value = st.selectbox('Поставьте оценку:', range(1, 11))
        if (st.button('Поставить')):
            try:
                response = requests.get(API_URL_RECS, json={"movie_id": movie_id, "score": selected_value})
                if response.status_code == 200:
                    draw_movies(response['movies'], 5, __file__)
                else:
                    st.error("Ошибка запроса.")
            except Exception as e:
                st.error(f"Ошибка подключения: {e}")
    
    st.title('Также смотрят:')

    try:
            response = requests.get(API_URL_RECS)
            if response.status_code == 200:
                draw_movies(response['movies'], 5, __file__)
            else:
                st.error("Ошибка запроса.")
    except Exception as e:
            st.error(f"Ошибка подключения: {e}")