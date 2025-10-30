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
st.title("アンケート")

if st.session_state.level == "B2":
    components.iframe("https://docs.google.com/forms/d/e/1FAIpQLScnrUoPQS0YD-sDT3GMvbTcsLvbeTHWcmK4tIj4cBd8aIoa8g/viewform?embedded=true", height=4500)
else:
    components.iframe("https://docs.google.com/forms/d/e/1FAIpQLSfrwEok1A49dAboYeYTpbhq4XZlX7mRzdVu8W2L2BRKSttxmA/viewform?embedded=true", height=4500)

if st.session_state.messages:
    log_text = ""
    for m in st.session_state.messages:
        if m["role"] != "system":
            prefix = "User" if m["role"] == "user" else "GPT"
            log_text += f"{prefix}: {m['content']}\n"

st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.button("ディスカッションページに戻る", on_click=lambda: go_to("chat"))
with col2:
    # ホームに戻る際にチャットをログをリセット
    st.button("ホームに戻る", on_click=lambda: (reset_chat(), go_to("home")))
