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

st.title(f"{st.session_state.level} レベル - ビデオ")
if st.session_state.level == "A2":
   st.markdown(
   """
   <iframe title="vimeo-player"
       src="https://player.vimeo.com/video/1057708086?h=118a6450d4"
       width="640"
       height="360"
       frameborder="0"
       referrerpolicy="strict-origin-when-cross-origin"
       allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media; web-share"
       allowfullscreen>
   </iframe>
   """,
   unsafe_allow_html=True
)
   
elif st.session_state.level == "B1":
    st.markdown(
   """
   <iframe title="vimeo-player"
       src="https://player.vimeo.com/video/1057779874?h=e96e0af70e"
       width="640"
       height="360"
       frameborder="0"
       referrerpolicy="strict-origin-when-cross-origin"
       allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media; web-share"
       allowfullscreen>
   </iframe>
   """,
   unsafe_allow_html=True
)
elif st.session_state.level == "B2":
    st.video("https://www.youtube.com/watch?v=YXn-eNPzlo8")
else:
    st.video("https://www.youtube.com/watch?v=1VA4rIkpSp8")

st.title(f"{st.session_state.level} レベル - 解説")

if st.session_state.level == "A2":
    # Step 1: 全文翻訳
    st.text("● 全文翻訳と解説")
    # with st.expander("本文と翻訳を表示"):
    explanation_text = load_text("explanation-text/exp_beach.txt")
    # st.write(explanation_text)

    st.markdown(
    f"""
    <div style="
        border:1px solid #999;
        padding:15px;
        border-radius:5px;
    ">
    {explanation_text}
    </div>
    """,
    unsafe_allow_html=True
    )

    # Step 2: 重要単語
    st.text("● 重要単語")
    vocab_data = load_json("explanation-text/vocab_beach.json")
    st.table(vocab_data)

    # Step 3: 重要フレーズ
    st.text("● 重要フレーズ")
    phrase_data = load_json("explanation-text/phrase_beach.json")
    st.table(phrase_data)

elif st.session_state.level == "B1":
    # Step 1: 全文翻訳
    st.text("● 全文翻訳と解説")
    # with st.expander("本文と翻訳を表示"):
    explanation_text = load_text("explanation-text/exp_embarrassing.txt")
        # st.write(explanation_text)
    st.markdown(
    f"""
    <div style="
        border:1px solid #999;
        padding:15px;
        border-radius:5px;
    ">
    {explanation_text}
    </div>
    """,
    unsafe_allow_html=True
    )

    # Step 2: 重要単語
    st.text("● 重要単語")
    vocab_data = load_json("explanation-text/vocab_embarrassing.json")
    st.table(vocab_data)

    # Step 3: 重要フレーズ
    st.text("● 重要フレーズ")
    phrase_data = load_json("explanation-text/phrase_embarrassing.json")
    st.table(phrase_data)

elif st.session_state.level == "B2":
    # Step 1: 全文翻訳
    st.text("● 全文翻訳と解説")
    # with st.expander("本文と翻訳を表示"):
    explanation_text = load_text("explanation-text/exp_dream.txt")
        # st.write(explanation_text)
    st.markdown(
    f"""
    <div style="
        border:1px solid #999;
        padding:15px;
        border-radius:5px;
    ">
    {explanation_text}
    </div>
    """,
    unsafe_allow_html=True
    )

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
    # with st.expander("本文と翻訳を表示"):
    explanation_text = load_text("explanation-text/exp_freight.txt")
        # st.write(explanation_text)
    st.markdown(
    f"""
    <div style="
        border:1px solid #999;
        padding:15px;
        border-radius:5px;
    ">
    {explanation_text}
    </div>
    """,
    unsafe_allow_html=True
    )
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
    if st.button("戻る", use_container_width=True):
        st.switch_page("pages/home.py")
with col2:
    # 次へボタン：クイズページに遷移
    if st.button("次へ", use_container_width=True, type="primary"):
        st.switch_page("pages/quiz.py")
