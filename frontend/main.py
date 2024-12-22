import streamlit as st
from pages import login, register, movies

USER_TABLE = {
    "Главная": movies
}

st.set_page_config(layout="wide")

if 'logged' not in st.session_state:
    st.session_state['logged'] = 0

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