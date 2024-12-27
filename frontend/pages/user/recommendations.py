import streamlit as st
import os
from util import draw_movies


def main():
    API_URL = f"{os.getenv('BACK_URL')}/recommendations"

    st.title("Ваши рекомендации:")

    try:
        response = st.session_state.session.get(API_URL)
        if response.status_code == 200:
            body = response.json()
            draw_movies(body, 6, __file__)
        elif response.status_code == 204:
            st.warning(
                "Вы новый пользователь, рекомендации пока не сформированы")
        else:
            st.error(response.status_code)
            st.error("Неправильные параметры.")
    except Exception as e:
        st.error(f"Ошибка подключения: {e}")
