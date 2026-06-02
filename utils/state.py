import streamlit as st

def init_state():
    defaults = {
        "selected_page": "Dashboard",
        "theme": "dark",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value