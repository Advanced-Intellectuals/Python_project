import streamlit as st
import requests

def main():
    API_URL_LOGOUT = "http://127.0.0.1:8000/logout"
    API_URL_SEARCH = "http://127.0.0.1:8000/search"
    API_URL_DELETE = "http://127.0.0.1:8000/delete_movie"

    title_column, exit_button_column = st.columns([6,1])

    with title_column:
        st.title("Удаление фильма")
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
    """
    search_bar = st.text_input("Введите название фильма:")
    if (search_bar):
        try:
                response = requests.post(API_URL_SEARCH, json={"search_title": search_bar})
                if response.status_code == 200:
                        draw_movies(response['movies'], 6, __file__)
                        st.rerun()
                else:
                    st.error("Неправильные параметры.")
        except Exception as e:
                st.error(f"Ошибка подключения: {e}")
    """

if __name__ == "__main__":
    main()