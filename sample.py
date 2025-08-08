import streamlit as st
import openai

# ページを記録する変数を初期化
if "page" not in st.session_state:
    st.session_state.page = 1

# 次へボタンの処理
def next_page():
    st.session_state.page += 1

# ページ1: TED動画ページ
if st.session_state.page == 1:
    st.title("TED動画を見る")
    # YouTubeリンク例（差し替え可）
    st.video("https://www.youtube.com/watch?v=3E7hkPZ-HTk")
    st.button("次へ", on_click=next_page)

# ページ2: 解説ページ
elif st.session_state.page == 2:
    st.title("解説")
    st.write("ここに解説文を記載します。")
    st.button("次へ", on_click=next_page)

# ページ3: ChatGPTとの会話ページ
elif st.session_state.page == 3:
    st.title("ChatGPTと会話")
    api_key = "YOUR_API_KEY_HERE"  # ←正しいAPIキーを貼り付け
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

    st.button("次へ", on_click=next_page)

# ページ4: アンケートページ
elif st.session_state.page == 4:
    st.title("アンケート")
    st.write("以下のリンクからアンケートにお答えください。")
    st.markdown("[Googleフォームはこちら](https://docs.google.com/forms/d/xxxxxx)")

