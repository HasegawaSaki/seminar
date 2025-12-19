import streamlit as st
import streamlit.components.v1 as components
from common import display_header, reset_chat, go_to

# --------セッション状態の初期化 --------
if "level" not in st.session_state:
    st.session_state.level = ""
if "messages2" not in st.session_state:
    st.session_state.messages2 = []

# -------- ページコンテンツ --------
display_header()
st.title("アンケート（2回目）")

components.iframe("https://docs.google.com/forms/d/e/1FAIpQLSe3xUPDVXSiCCPA9DlvuFUxAJ4CasXkhMjTq7PxKRLZTjDP3Q/viewform?usp=dialog", height=5500)
# if st.session_state.level == "A2":
#     components.iframe("https://docs.google.com/forms/d/e/1FAIpQLScpPh7R37lcF8rnAWSX3zPDIictXRkf_RBcQSr8Pz0s-TUJrQ/viewform?embedded=true", height=4500)
# elif st.session_state.level == "B1":
#     components.iframe("https://docs.google.com/forms/d/e/1FAIpQLSeO8CZ31rY0mNmJFx5eJ0ritfvkXZE2bZVl9YJZIg9Ddye3pg/viewform?usp=dialog", height=4500)
# elif st.session_state.level == "B2":
#     components.iframe("https://docs.google.com/forms/d/e/1FAIpQLScnrUoPQS0YD-sDT3GMvbTcsLvbeTHWcmK4tIj4cBd8aIoa8g/viewform?embedded=true", height=4500)
# else:
#     components.iframe("https://docs.google.com/forms/d/e/1FAIpQLSfrwEok1A49dAboYeYTpbhq4XZlX7mRzdVu8W2L2BRKSttxmA/viewform?embedded=true", height=4500)

if st.session_state.messages2:
    log_text = ""
    for m in st.session_state.messages2:
        if m["role"] != "system":
            prefix = "User" if m["role"] == "user" else "GPT"
            log_text += f"{prefix}: {m['content']}\n"

st.markdown("---")
col1, col2 = st.columns(2)

col1, col2 = st.columns([1, 1])

with col1:
    # 戻るボタン：ディスカッション2に戻る
    if st.button("戻る", use_container_width=True):
        st.switch_page("pages/discussion_improve.py")
with col2:
    # 終了するボタン：終了ページに遷移
    if st.button("終了する", use_container_width=True, type="primary"):
        st.switch_page("pages/end.py")
