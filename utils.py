import streamlit as st

def go_to(page_name, route=None):
    if route:
        st.session_state.route = route
    st.session_state.page = page_name

def set_role(role):
    st.session_state.role = role

def go_to_and_clear_chat(page_name, route=None):
    if "messages" in st.session_state:
        del st.session_state.messages
    go_to(page_name, route)
