import streamlit as st
from pages.auth import login, register
from pages.cinema import all_movies, recs, search, personal

USER_TABLE = {
    "Главная": all_movies,
    "Рекомендации": recs,
    "Поиск": search,
    "Личный кабинет": personal
}

st.set_page_config(layout="wide")

if 'logged' not in st.session_state:
    st.session_state['logged'] = 1

if 'auth_page' not in st.session_state:
    st.session_state['auth_page'] = 'login'

def main():
    if st.session_state['logged'] == 0:
        if st.session_state['auth_page'] == 'login':
            login.main()
        else:
            register.main()
    if st.session_state['logged'] == 1:
        page = st.sidebar.radio("Выберите",list(USER_TABLE.keys()))
        USER_TABLE[page].main()

if __name__ == "__main__":
    main()