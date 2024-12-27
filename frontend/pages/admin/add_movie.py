import streamlit as st
import requests
import uuid
import os


def main():
    API_URL_LOGOUT = f"{os.getenv('BACK_URL')}/logout"
    API_URL_ADD = f"{os.getenv('BACK_URL')}/add_movie"
    title_column, exit_button_column = st.columns([6, 1])

    with title_column:
        st.title("Загрузка фильма")
    with exit_button_column:
        if st.button("ВЫХОД"):
            try:
                response = st.session_state.session.post(API_URL_LOGOUT)
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
        options=['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy', 'Romance', 'Drama',
                 'Action', 'Crime', 'Thriller', 'Horror', 'Mystery', 'Sci-Fi', 'War', 'Musical',
                 'Documentary', 'IMAX', 'Western', 'Film-Noir']

    )

    save_dir = 'tmp'
    os.makedirs(save_dir, exist_ok=True)

    video_file = st.file_uploader("Загрузка видео", type=["mp4", "mov", "avi"])

    if video_file:
        file_path = os.path.join(save_dir, video_file.name)
        with open(file_path, "wb") as file1:
            file1.write(video_file.getbuffer())

    preview_image = st.file_uploader(
        "Загрузка фото", type=["jpg", "jpeg", "png"])

    if preview_image:
        preview_path = os.path.join(save_dir, preview_image.name)
        with open(preview_path, "wb") as file2:
            file2.write(preview_image.getbuffer())

    if st.button("Загрузить"):
        if name and year and genres and preview_image and video_file:
            try:
                preview = str(uuid.uuid4())
                file = str(uuid.uuid4())
                st.session_state.minio_server.put_file(preview_path, preview)
                st.session_state.minio_server.put_file(file_path, file)

                if os.path.exists(file_path):
                    os.remove(file_path)

                if os.path.exists(preview_path):
                    os.remove(preview_path)

                response = st.session_state.session.post(API_URL_ADD, json={"name": name,
                                                                            "genres": genres,
                                                                            "year": year,
                                                                            "preview": preview,
                                                                            "file": file})
                if response.status_code == 201:
                    st.success('Фильм добавлен!')
                else:
                    st.error("Неправильные параметры.")
            except Exception as e:
                st.error(f"Ошибка подключения: {e}")
        else:
            st.warning("Пожалуйста заполните все поля")
