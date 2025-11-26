import streamlit as st

# --------セッション状態の初期化 --------
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

# ページを定義（タイトルを大文字に設定）
welcome_page = st.Page("pages/welcome.py", title="本アプリについて")
home_page = st.Page("pages/home.py", title="ホーム")
video_page = st.Page("pages/video.py", title="ビデオ")
quiz_page = st.Page("pages/quiz.py", title="クイズ")
discussion_page = st.Page("pages/discussion.py", title="ディスカッション")
survey_page = st.Page("pages/survey.py", title="アンケート")
# ナビゲーションを設定
pg = st.navigation([welcome_page, home_page, video_page, quiz_page, discussion_page, survey_page])

# 選択されたページを実行
pg.run()
