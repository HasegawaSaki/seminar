import streamlit as st
import openai

# ページ番号をセッションに保持
if "page" not in st.session_state:
    st.session_state.page = 1

def next_page():
    if st.session_state.page < 4:
        st.session_state.page += 1

def prev_page():
    if st.session_state.page > 1:
        st.session_state.page -= 1

# ページ1: TED動画ページ
if st.session_state.page == 1:
    st.title("TED動画を見る")
    st.video("https://www.youtube.com/watch?v=3E7hkPZ-HTk")
    col1, col2 = st.columns(2)
    with col1:
        st.button("戻る", on_click=prev_page, disabled=True)  # 最初のページは戻れない
    with col2:
        st.button("次へ", on_click=next_page)

# ページ2: 解説ページ
elif st.session_state.page == 2:
    st.title("解説")
    st.write("ここに解説文を記載します。")
    col1, col2 = st.columns(2)
    with col1:
        st.button("戻る", on_click=prev_page)
    with col2:
        st.button("次へ", on_click=next_page)

# ページ3: ChatGPTとの会話ページ
elif st.session_state.page == 3:
    st.title("ChatGPTと会話")
    api_key = "YOUR_API_KEY_HERE"  # ←正しいAPIキーに置き換える
    openai.api_key = api_key

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 過去の会話を表示
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ユーザー入力
    if prompt := st.chat_input("質問や感想を入力してください"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # ChatGPT API呼び出し
        with st.chat_message("assistant"):
            with st.spinner("ChatGPTが考え中..."):
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state.messages
                )
                reply = response["choices"][0]["message"]["content"]
                st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

    col1, col2 = st.columns(2)
    with col1:
        st.button("戻る", on_click=prev_page)
    with col2:
        st.button("次へ", on_click=next_page)

# ページ4: アンケートページ
elif st.session_state.page == 4:
    st.title("アンケート")
    st.write("以下のリンクからアンケートにお答えください。")
    st.markdown("[Googleフォームはこちら](https://docs.google.com/forms/d/xxxxxx)")

    col1, col2 = st.columns(2)
    with col1:
        st.button("戻る", on_click=prev_page)
    with col2:
        st.button("次へ", on_click=next_page, disabled=True)  # 最終ページは次へ無効
