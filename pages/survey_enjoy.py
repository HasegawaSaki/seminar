import streamlit as st
import streamlit.components.v1 as components
from common import display_header, reset_chat, go_to

# --------セッション状態の初期化 --------
if "level" not in st.session_state:
    st.session_state.level = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------- ページコンテンツ --------
display_header()
st.title("アンケート（1回目）")

if st.session_state.level == "A2":
    components.iframe("https://docs.google.com/forms/d/e/1FAIpQLScpPh7R37lcF8rnAWSX3zPDIictXRkf_RBcQSr8Pz0s-TUJrQ/viewform?embedded=true", height=2300)
elif st.session_state.level == "B1":
    components.iframe("https://docs.google.com/forms/d/e/1FAIpQLSeO8CZ31rY0mNmJFx5eJ0ritfvkXZE2bZVl9YJZIg9Ddye3pg/viewform?usp=dialog", height=2300)
elif st.session_state.level == "B2":
    components.iframe("https://docs.google.com/forms/d/e/1FAIpQLSeiNkAVdv5YOBg1QIAo6ZFZmHoMn41A93PWQuFYALy9vFhBcw/viewform?usp=dialog", height=2300)
else:
    components.iframe("https://docs.google.com/forms/d/e/1FAIpQLSfrwEok1A49dAboYeYTpbhq4XZlX7mRzdVu8W2L2BRKSttxmA/viewform?embedded=true", height=2300)

if st.session_state.messages:
    log_text = ""
    for m in st.session_state.messages:
        if m["role"] != "system":
            prefix = "User" if m["role"] == "user" else "GPT"
            log_text += f"{prefix}: {m['content']}\n"

st.markdown("---")
col1, col2 = st.columns(2)

col1, col2 = st.columns([1, 1])

with col1:
    # 戻るボタン：ディスカッションに戻る
    if st.button("戻る", use_container_width=True):
        st.switch_page("pages/discussion_enjoy.py")
with col2:
    # 次へボタン：ディスカッション2ページに遷移
    if st.button("次へ", use_container_width=True, type="primary"):
        st.switch_page("pages/discussion_improve.py")
