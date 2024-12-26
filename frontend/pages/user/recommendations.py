import streamlit as st
import requests
from util import draw_movies

def main():
    API_URL = "http://127.0.0.1:8000/recommendations"

    st.title("Ваши рекомендации:")

    try:
                response = requests.post(API_URL)
                if response.status_code == 200:
                        draw_movies(response['movies'], 6, __file__)
                        st.rerun()
                else:
                    st.error("Неправильные параметры.")
    except Exception as e:
                st.error(f"Ошибка подключения: {e}")

if __name__ == "__main__":
    main()