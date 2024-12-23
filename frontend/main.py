import streamlit as st
from pages.user import movies, recommendations, watched, search, movie
from pages.auth import login, register
from pages.admin import add_movie

st.set_page_config(layout="wide")

USER_TABLE = {
    "Главная": movies,
    "Рекомендации": recommendations,
    "Поиск": search,
    "Личный кабинет": watched
}

if 'logged' not in st.session_state:
    st.session_state['logged'] = 1

if 'auth_page' not in st.session_state:
    st.session_state['auth_page'] = 'login'

if 'watching_movie' not in st.session_state:
    st.session_state['watching_movie'] = 0

if 'previous_page' not in st.session_state:
    st.session_state['previous_page'] = list(USER_TABLE.keys())[0]

def main():
    if st.session_state['logged'] == 0:
        if st.session_state['auth_page'] == 'login':
            login.main()
        else:
            register.main()  
    elif st.session_state['logged'] == 1:
        if st.session_state['watching_movie'] == 0:
            page = st.sidebar.radio("Выберите", list(USER_TABLE.keys()), index=list(USER_TABLE.keys()).index(st.session_state['previous_page']))
            USER_TABLE[page].main()
        else:
            movie.main()

if __name__ == "__main__":
    main()