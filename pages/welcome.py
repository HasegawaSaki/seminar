import streamlit as st

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

# Welcome Page Content
# カスタムCSS
st.markdown("""
<style>
.welcome-header {
    text-align: center;
    padding: 2rem 0;
    background: #FB323B;
    border-radius: 15px;
    margin-bottom: 2rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.welcome-title {
    color: white;
    font-size: 3em;
    font-weight: bold;
    margin: 0;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}
.welcome-subtitle {
    color: #f0f0f0;
    font-size: 1.5em;
    margin-top: 0.5rem;
}
.welcome-description {
    text-align: center;
    font-size: 1.3em;
    margin: 2rem 0;
    line-height: 1.6;
}
.feature-card {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    margin-bottom: 1rem;
    border-left: 4px solid #FB323B;
    transition: transform 0.2s;
}
.feature-card:hover {
    transform: translateX(5px);
}
.feature-icon {
    font-size: 2em;
    margin-right: 0.5rem;
}
.feature-title {
    font-size: 1.3em;
    font-weight: bold;
    color: #333;
    margin-bottom: 0.5rem;
}
.feature-text {
    color: #666;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# ヘッダー
st.markdown("""
<div class='welcome-header'>
    <h1 class='welcome-title'>AI English Learning Tool</h1>
</div>
""", unsafe_allow_html=True)

# 説明文
st.markdown("""
<div class='welcome-description'>
    英語のビデオを視聴してAIとディスカッションを<br>
    することにより英語学習をサポートします。
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 機能紹介
st.markdown("""
<div class='feature-card'>
    <div><span class='feature-title'>① ビデオの視聴</span></div>
    <div class='feature-text'>レベル別の英語のビデオを視聴</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='feature-card'>
    <div><span class='feature-title'>② 動画の解説</span></div>
    <div class='feature-text'>重要単語やフレーズの学習、全文翻訳で内容理解をサポート</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='feature-card'>
    <div><span class='feature-title'>③ AIとディスカッション</span></div>
    <div class='feature-text'>動画の内容について英語で会話<br>モードの異なる2つのディスカッションに取り組んでいただきます。</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>" * 2, unsafe_allow_html=True)

# スタートボタンを中央に配置
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("スタート", use_container_width=True, type="primary"):
        st.switch_page("pages/home.py")
