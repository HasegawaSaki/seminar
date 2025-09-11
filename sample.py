import streamlit as st
import openai
import requests
import base64
import datetime
from datetime import datetime
import zoneinfo

# GitHub関数
def push_to_github(filename, content):
    token = st.secrets["GITHUB_TOKEN"]
    repo = st.secrets["GITHUB_REPO"]
    branch = st.secrets["GITHUB_BRANCH"]

    url = f"https://api.github.com/repos/{repo}/contents/{filename}"
    message = f"Add chat log {filename}"
    b64_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")

    headers = {"Authorization": f"token {token}"}
    data = {
        "message": message,
        "content": b64_content,
        "branch": branch
    }

    response = requests.put(url, headers=headers, json=data)
    return response
# --------ページ遷移管理 --------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "username" not in st.session_state:
    st.session_state.username = ""
if "purpose" not in st.session_state:
    st.session_state.purpose = ""
if "level" not in st.session_state:
    st.session_state.level = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

def go_to(page, level=None, purpose=None):
    if level:
        st.session_state.level = level
    if purpose:
        st.session_state.purpose = purpose
    st.session_state.page = page

# --------プロンプト分岐--------
def get_system_prompt(level, purpose):
    if level == "B2" and purpose == "楽しく会話":
        return """ここに B2 ✖️ 楽しく会話 用のプロンプトを貼る"""

    elif level == "B2" and purpose == "英語力の向上":
        return """ここに B2 ✖️ 英語力の向上 用のプロンプトを貼る"""

    elif level == "C1" and purpose == "楽しく会話":
        return """ここに C1 ✖️ 楽しく会話 用のプロンプトを貼る"""

    elif level == "C1" and purpose == "英語力の向上":
        return """ここに C1 ✖️ 英語力の向上 用のプロンプトを貼る"""


# ================== 各ページ描画 ==================
def home_page():
    st.title("ホーム")
    st.session_state.username = st.text_input("名前を入力してください", placeholder="例）山田太郎")

    purpose = st.radio("ディスカッションの目的を選んでください", ["楽しく会話", "英語力の向上"], key="purpose")

    def go_with_check(level):
        if not st.session_state.username.strip():
            st.warning("⚠️ 名前を入力してください")
        else:
            go_to("video", level=level, purpose=purpose)

    col1, col2 = st.columns(2)
    with col1:
        st.button("B2レベル", on_click=lambda: go_with_check("B2"))
    with col2:
        st.button("C1レベル", on_click=lambda: go_with_check("C1"))


def video_page():
    st.title(f"{st.session_state.level} レベル - TED動画")
    if st.session_state.level == "B2":
        st.video("https://www.youtube.com/watch?v=YXn-eNPzlo8")
    else:
        st.video("https://www.youtube.com/watch?v=1VA4rIkpSp8")

    col1, col2 = st.columns(2)
    with col1:
        st.button("戻る", on_click=lambda: go_to("home"))
    with col2:
        st.button("次へ", on_click=lambda: go_to("explanation"))


def explanation_page():
    st.title(f"{st.session_state.level} レベル - 解説")
    if st.session_state.level == "B2":
        st.markdown("ここにB2用の解説文を入れます。")
    else:
        st.markdown("ここにC1用の解説文を入れます。")

    col1, col2 = st.columns(2)
    with col1:
        st.button("戻る", on_click=lambda: go_to("video"))
    with col2:
        st.button("次へ", on_click=lambda: go_to("chat"))


def chat_page():
    st.title(f"{st.session_state.level} - {st.session_state.purpose}")
    api_key = st.secrets["API_KEY"]
    client = openai.OpenAI(api_key=api_key)

    if not st.session_state.messages:
        st.session_state.messages = [
            {"role": "system", 
             "content": get_system_prompt(st.session_state.level, st.session_state.purpose)},
            {"role": "assistant", "content": "Hey! What did you think about the TED Talk?"}
        ]
    # 過去の会話を表示
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # ユーザー入力
    if prompt := st.chat_input("質問や感想を入力してください"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("ChatGPTが考え中..."):
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state.messages
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

    col1, col2 = st.columns(2)
    with col1:
        st.button("戻る", on_click=lambda: go_to("explanation"))
    with col2:
        st.button("次へ", on_click=lambda: go_to("survey"))


def survey_page():
    st.title("アンケート")
    st.markdown("[Googleフォームはこちら](https://docs.google.com/forms/d/xxxxxx)")

    if st.session_state.messages:
        log_text = ""
        for m in st.session_state.messages:
            if m["role"] != "system":
                prefix = "User" if m["role"] == "user" else "GPT"
                log_text += f"{prefix}: {m['content']}\n"

        if st.button("🚀 ログを送信（GitHubに保存）"):
            jst = zoneinfo.ZoneInfo("Asia/Tokyo")
            now = datetime.now(jst)
            filename = f"log/{st.session_state.username}_{now.strftime('%Y%m%d_%H%M%S')}.txt"
            response = push_to_github(filename, log_text)
            if response.status_code in [200, 201]:
                st.success(f"✅ {filename} をGitHubに保存しました！")
            else:
                st.error(f"❌ 送信失敗: {response.json()}")

    st.button("ホームに戻る", on_click=lambda: go_to("home"))


# ================== ページ遷移 ==================
if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "video":
    video_page()
elif st.session_state.page == "explanation":
    explanation_page()
elif st.session_state.page == "chat":
    chat_page()
elif st.session_state.page == "survey":
    survey_page()
