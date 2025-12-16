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

# Discussion2用のセッション状態
if "messages2" not in st.session_state:
    st.session_state.messages2 = []
if "chat_start_time2" not in st.session_state:
    st.session_state.chat_start_time2 = None
if "chat_duration2" not in st.session_state:
    st.session_state.chat_duration2 = None
if "chat_timer_start2" not in st.session_state:
    st.session_state.chat_timer_start2 = None
if "input_counter2" not in st.session_state:
    st.session_state.input_counter2 = 0
if "user_utter_index2" not in st.session_state:
    st.session_state.user_utter_index2 = 1

# ページを定義（タイトルを大文字に設定）
welcome_page = st.Page("pages/welcome.py", title="本アプリについて")
home_page = st.Page("pages/home.py", title="ホーム")
video_page = st.Page("pages/video.py", title="ビデオ")
quiz_page = st.Page("pages/quiz.py", title="クイズ")
discussion_page = st.Page("pages/discussion_enjoy.py", title="ディスカッション（楽しく会話）")
survey_page = st.Page("pages/survey_enjoy.py", title="アンケート（楽しく会話）")
discussion2_page = st.Page("pages/discussion_improve.py", title="ディスカッション（英語力の向上）")
survey2_page = st.Page("pages/survey_improve.py", title="アンケート（英語力の向上）")
end_page = st.Page("pages/end.py", title="終了")
# ナビゲーションを設定
pg = st.navigation([welcome_page, home_page, video_page, quiz_page, discussion_page, survey_page, discussion2_page, survey2_page, end_page])

# 選択されたページを実行
pg.run()
