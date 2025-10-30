import streamlit as st
from common import display_header, tutorial_video, load_text, load_json, reset_chat, go_to

# --------セッション状態の初期化 --------
if "level" not in st.session_state:
    st.session_state.level = ""
if "tutorial_seen01" not in st.session_state:
   st.session_state["tutorial_seen01"] = False

# -------- ページコンテンツ --------
display_header()

if not st.session_state["tutorial_seen01"]:
   tutorial_video()

st.warning("動画を視聴後、解説を読んでからページ右下の「次へ」ボタンを押し、クイズ画面に進んでください。")

st.title(f"{st.session_state.level} レベル - TED動画")
if st.session_state.level == "B2":
    st.video("https://www.youtube.com/watch?v=YXn-eNPzlo8")
else:
    st.video("https://www.youtube.com/watch?v=1VA4rIkpSp8")

st.title(f"{st.session_state.level} レベル - 解説")

if st.session_state.level == "B2":
    # Step 1: 全文翻訳
    st.text("全文翻訳と解説")
    with st.expander("本文と翻訳を表示"):
        explanation_text = load_text("explanation-text/exp_dream.txt")
        st.write(explanation_text)

    # Step 2: 重要単語
    st.text("● 重要単語")
    vocab_data = load_json("explanation-text/vocab_dream.json")
    st.table(vocab_data)

    # Step 3: 重要フレーズ
    st.text("● 重要フレーズ")
    phrase_data = load_json("explanation-text/phrase_dream.json")
    st.table(phrase_data)

else:
    # Step 1: 全文翻訳
    st.text("● 全文翻訳と解説")
    with st.expander("本文と翻訳を表示"):
        explanation_text = load_text("explanation-text/exp_freight.txt")
        st.write(explanation_text)

    # Step 2: 重要単語
    st.text("● 重要単語")
    vocab_data = load_json("explanation-text/vocab_freight.json")
    st.table(vocab_data)

    # Step 3: 重要フレーズ
    st.text("● 重要フレーズ")
    phrase_data = load_json("explanation-text/phrase_freight.json")
    st.table(phrase_data)


col1, col2 = st.columns([1, 1])

with col1:
    # 戻るボタン：チャットリセットしてホームに戻る
    if st.button("戻る", use_container_width=True, type="primary"):
        reset_chat()
        st.switch_page("pages/1_home.py")
with col2:
    # 次へボタン：クイズページに遷移
    if st.button("次へ", use_container_width=True, type="primary"):
        st.switch_page("pages/3_quiz.py")
