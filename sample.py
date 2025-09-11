import streamlit as st
import datetime
from datetime import datetime
import zoneinfo

from views import home_view, route1_views, route2_views

# セッション変数の初期化
if "route" not in st.session_state:
    st.session_state.route = None
if "page" not in st.session_state:
    st.session_state.page = "home"
if "role" not in st.session_state:
    st.session_state.role = None
if "username" not in st.session_state:
    st.session_state.username = ""
if "date" not in st.session_state:
    jst = zoneinfo.ZoneInfo("Asia/Tokyo")
    st.session_state.date = datetime.now(jst).strftime("%Y%m%d")

# ページルーター
if st.session_state.page == "home":
    home_view.render()

# --- Route 1 ---
elif st.session_state.page == "video1":
    route1_views.render_video()
elif st.session_state.page == "explanation1":
    route1_views.render_explanation()
elif st.session_state.page == "chat1":
    route1_views.render_chat()
elif st.session_state.page == "survey":
    route1_views.render_survey()

# --- Route 2 ---
elif st.session_state.page == "video2":
    route2_views.render_video()
elif st.session_state.page == "explanation2":
    route2_views.render_explanation()
elif st.session_state.page == "chat2":
    route2_views.render_chat()
elif st.session_state.page == "survey2":
    route2_views.render_survey()