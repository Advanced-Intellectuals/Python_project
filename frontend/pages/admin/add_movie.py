import streamlit as st
import requests
import uuid
import minio_server

def main():
    API_URL_LOGOUT = "http://127.0.0.1:8000/logout"
    API_URL_ADD = "http://127.0.0.1:8000/add_movie"
    title_column, exit_button_column = st.columns([6,1])

    with title_column:
        st.title("Загрузка фильма")
    with exit_button_column:
        if st.button("ВЫХОД"):
            try:
                response = requests.post(API_URL_LOGOUT)
                if response.status_code == 200:
                    st.session_state['logged'] = 0
                    st.rerun()
                else:
                    st.error("Неправильные параметры.")
            except Exception as e:
                st.error(f"Ошибка подключения: {e}")


    name = st.text_input("Название фильма")

    year = st.number_input("Год", min_value=1900, max_value=2100, step=1)

    genres = st.multiselect(
        "Жанры",
        options=["Action", "Adventure", "Comedy", "Drama", "Horror", "Sci-Fi", "Thriller", "Romance", "Documentary"]
    )

    video_file = st.file_uploader("Загрузка видео", type=["mp4", "mov", "avi"])

    preview_image = st.file_uploader("Загрузка фото", type=["jpg", "jpeg", "png"])

    if st.button("Загрузить"):
        if name and year and genres and preview_image and video_file:
            try:
                preview = str(uuid.uuid4())
                file = str(uuid.uuid4())
                response = requests.post(API_URL_ADD, json={"name": name, 
                                                                "genres": genres,
                                                                "year": year,
                                                                "preview": preview,
                                                                "file": file})
                if response.status_code == 200:
                    minio_server.MinioServer().put_file(preview_image, preview)
                    minio_server.MinioServer().put_file(video_file, file)
                    st.success('Фильм добавлен!')
                else:
                    st.error("Неправильные параметры.")
            except Exception as e:
                st.error(f"Ошибка подключения: {e}")
        else:
            st.warning("Пожалуйста заполните все поля")

if __name__ == "__main__":
    main()