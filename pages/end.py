import streamlit as st
from common import display_header, reset_chat

# -------- ページコンテンツ --------

# ヘッダー
st.markdown("""
<div class='welcome-header'>
    <h2 class='welcome-title'>ご協力ありがとうございました！</h2>
</div>
""", unsafe_allow_html=True)

# 説明文
st.markdown("""
<div class='welcome-description'>
    これでユーザー評価は終了です。
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

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
    font-size: 1em;
    font-weight: bold;
    margin: 10;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}
.welcome-description {
    text-align: center;
    font-size: 1.3em;
    margin: 2rem 0;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)
