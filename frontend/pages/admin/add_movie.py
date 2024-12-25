import streamlit as st

def main():
    title_column, exit_button_column = st.columns([6,1])

    with title_column:
        st.title("Загрузка фильма")
    with exit_button_column:
        if st.button("ВЫХОД"):
            st.session_state['logged'] = 0
            st.rerun()

    name = st.text_input("Название фильма")

    year = st.number_input("Год", min_value=1900, max_value=2100, step=1)

    genres = st.multiselect(
        "Жанры",
        options=["Action", "Adventure", "Comedy", "Drama", "Horror", "Sci-Fi", "Thriller", "Romance", "Documentary"],
        default=["Action"]
    )

    video_file = st.file_uploader("Загрузка видео", type=["mp4", "mov", "avi"])

    preview_image = st.file_uploader("Загрузка фото", type=["jpg", "jpeg", "png"])

    if st.button("Загрузить"):
        if name and year and genres and preview_image and video_file:
            st.write("Хорошо!")
        else:
            st.warning("Пожалуйста заполните все поля")

if __name__ == "__main__":
    main()