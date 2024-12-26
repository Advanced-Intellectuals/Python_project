import streamlit as st
import requests
from util import draw_movies

def main():
    API_URL = "http://127.0.0.1:8000/movies"

    movie_grid, params = st.columns([6, 1])

    with params:
        st.write("Дата выхода фильма")
        date1, symb, date2 = st.columns([2,1,2], vertical_alignment="bottom")

        with date1:
            number1 = st.number_input("ОТ:", value=1900, step=1)

        with symb:
            st.write("--")

        with date2:
            number2 = st.number_input("ДО:", value=2024, step=1)

        options = ["Option 1", "Option 2", "Option 3"]
        selected_options = st.multiselect("Жанры:", options)

    if number1 and number2:
        with movie_grid:
            try:
                response = requests.post(API_URL, json={"page_number": st.session_state['movie_page'], 
                                                                "page_size": 30,
                                                                "start_year": number1,
                                                                "end_year": number2,
                                                                "genres": selected_options})
                if response.status_code == 200:
                        draw_movies(response['movies'], 6, __file__)
                        st.rerun()
                else:
                    st.error("Неправильные параметры.")
            except Exception as e:
                st.error(f"Ошибка подключения: {e}")

    page_button_cont1, page_button_cont2 = st.columns(2)
    with page_button_cont1:
        if st.button("Предыдущая страница"):
            if st.session_state['movie_page'] != 0:
                st.session_state['movie_page'] = st.session_state['movie_page']-1
            else:
                st.warning("Начальная страница")
    with page_button_cont2:
        if st.button("Следующая страница"):
            st.session_state['movie_page'] = st.session_state['movie_page']+1
            

if __name__ == "__main__":
    main()