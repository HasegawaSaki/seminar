import streamlit as st
from pages.welcome import welcome_page
from pages.home import home_page
from pages.video import video_page
from pages.explanation import explanation_page
from pages.chat import chat_page
from pages.survey import survey_page

# --------ページ遷移管理 --------
if "page" not in st.session_state:
    st.session_state.page = "welcome"
if "username" not in st.session_state:
    st.session_state.username = ""
if "purpose" not in st.session_state:
    st.session_state.purpose = "楽しく会話"
if "level" not in st.session_state:
    st.session_state.level = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_start_time" not in st.session_state:
    st.session_state.chat_start_time = None
if "chat_duration" not in st.session_state:
    st.session_state.chat_duration = None
if "chat_timer_start" not in st.session_state:
    st.session_state.chat_timer_start = None
if "show_warning" not in st.session_state:
   st.session_state.show_warning = False

# -------- ページ遷移 --------
if st.session_state.page == "welcome":
    welcome_page()
elif st.session_state.page == "home":
    home_page()
elif st.session_state.page == "video":
    video_page()
elif st.session_state.page == "explanation":
    explanation_page()
elif st.session_state.page == "chat":
    chat_page()
elif st.session_state.page == "survey":
    survey_page()
