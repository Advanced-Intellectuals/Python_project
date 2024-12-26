import streamlit as st
import requests
from util import draw_movies

def main():
    API_URL_WATCHED = "http://127.0.0.1:8000/watched"
    API_URL_LOGOUT = "http://127.0.0.1:8000/logout"

    _, exit_button_column = st.columns([8,1], vertical_alignment="top")
    
    with exit_button_column:
        exit_button = st.button("Выйти из аккаунта")
    if exit_button:
        try:
                response = requests.post(API_URL_LOGOUT)
                if response.status_code == 200:
                    st.session_state['logged'] = 0
                    st.rerun()
                else:
                    st.error("Неправильные параметры.")
        except Exception as e:
                st.error(f"Ошибка подключения: {e}")
        
    
    st.title("Просмотренные фильмы:")
    try:
                response = requests.post(API_URL_WATCHED)
                if response.status_code == 200:
                        draw_movies(response['movies'], 6, __file__)
                        st.rerun()
                else:
                    st.error("Неправильные параметры.")
    except Exception as e:
                st.error(f"Ошибка подключения: {e}")

if __name__ == "__main__":
    main()