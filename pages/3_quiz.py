import streamlit as st
import streamlit.components.v1 as components
from common import display_header, tutorial_quiz, go_to

# --------セッション状態の初期化 --------
if "level" not in st.session_state:
    st.session_state.level = ""
if "tutorial_seen02" not in st.session_state:
    st.session_state["tutorial_seen02"] = False

# -------- ページコンテンツ --------
display_header()

# ページ読み込み時に一番上にスクロール
components.html("""
<script>
    window.parent.document.querySelector('section.main').scrollTo(0, 0);
</script>
""", height=50)

if not st.session_state["tutorial_seen02"]:
    tutorial_quiz()

st.title(f"{st.session_state.level} レベル - クイズ")

form_urls = {
"A2": "https://docs.google.com/forms/d/e/1FAIpQLSd4X5HctpCM9yNdjARTXqGRVwEcQMHB2UY_GON6teDTjb_myg/viewform?embedded=true",
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

col1, col2 = st.columns([1, 1])

with col1:
    # 戻るボタン：チャットリセットしてホームに戻る
    if st.button("戻る", use_container_width=True):
        st.switch_page("pages/2_video.py")
with col2:
    # 次へボタン：クイズページに遷移
    if st.button("次へ", use_container_width=True, type="primary"):
        st.switch_page("pages/4_discussion.py")
