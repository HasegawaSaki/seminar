import streamlit as st
import streamlit.components.v1 as components
from common import display_header, tutorial_quiz, go_to

def explanation_page():
    display_header()
    if "tutorial_seen02" not in st.session_state:
        st.session_state["tutorial_seen02"] = False
    if not st.session_state["tutorial_seen02"]:
        tutorial_quiz()
    st.title(f"{st.session_state.level} レベル - クイズ")
    form_urls = {
    "B2": "https://docs.google.com/forms/d/e/1FAIpQLSeQ4nnfuB731SUGSUT_JjK80_3IyZuUmFuXCZCS5KJNXS4Qwg/viewform?embedded=true",
    "C1": "https://docs.google.com/forms/d/e/1FAIpQLScQkodloIAKuZ37kWzadb6-FTzP1YleRskhrodAoS1BQROTIg/viewform?embedded=true"
    }
    form_html = f"""
    <iframe src="{form_urls[st.session_state.level]}" width="100%" height="1200" frameborder="0" marginheight="0" marginwidth="0" scrolling="yes">
    読み込んでいます…
    </iframe>
    """

    # アプリ内に埋め込む（iframe）
    components.html(form_html, height=1200)

    col1, col2 = st.columns(2)

    with col1:
        st.button("戻る", on_click=lambda: go_to("video"))
    with col2:
        st.button("次へ(ディスカッションに移動する)", on_click=lambda: go_to("chat"))
