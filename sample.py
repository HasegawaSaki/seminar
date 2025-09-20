import streamlit as st
import openai
import json
import requests
import base64
from datetime import datetime
import zoneinfo

# --------GitHub関数--------
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
    st.session_state.purpose = "楽しく会話"
if "level" not in st.session_state:
    st.session_state.level = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_start_time" not in st.session_state:
    st.session_state.chat_start_time = None
if "chat_duration" not in st.session_state:
    st.session_state.chat_duration = None
if "chat_timer_start" not in st.session_state:
    st.session_state.chat_timer_start = None

def go_to(page, level=None, purpose=None):
    if level:
        st.session_state.level = level
    if purpose:
        st.session_state.purpose = purpose
    st.session_state.page = page

# --------チャットリセット--------
def reset_chat():
    if "messages" in st.session_state:
        st.session_state.messages = []
        st.session_state.username = ""
        st.session_state.chat_start_time = None
        st.session_state.chat_timer_start = None
        st.session_state.chat_duration = None
        
# --------プロンプト分岐--------
def get_system_prompt(level, purpose):
    if purpose == '楽しく会話':
        role_prompt = '''
        Role: Friendly Conversational Partner
        Goal: Have a fun and empathetic conversation.
        Output format:
        1. Empathize with the user's feelings and comments.
        2. Share your personal feelings and experiences.
        3. Ask follow-up questions to keep the conversation going.
        Keep answers very brief (1-2 sentences).
        1 sentence have 15 words or less.
'''
    else:
        role_prompt = '''
        Role: English Language Tutor
        Goal: Improve the user's English skills based on a video's content.
        Output format:
        1. If the user answers incorrectly, Correct the user's grammar and vocabulary mistakes.
        correct version : ~
        2. Deepen the user's understanding of the video's content.
'''
    if level == "B2" and purpose == "楽しく会話":
        with open("script/scr-dream.txt", "r", encoding="utf-8") as f:
            script = f.read()
        with open("sample-conversation/conv-dream.txt", "r", encoding="utf-8") as f:
            conversation_example = f.read()
        
        return f'''
<Rules>
- We had a conversation about the topic.
- The conversation starts with the user answering the question, "what did you think of the TED Talk about ?"
- You reply shortly (2~3 sentences),
- Keep the English clear
<Role>
{role_prompt}
{script}
{conversation_example}
'''

    elif level == "B2" and purpose == "英語力の向上":
        with open("script/scr-dream.txt", "r", encoding="utf-8") as f:
            script = f.read()
        with open("sample-conversation/conv-dream.txt", "r", encoding="utf-8") as f:
            conversation_example = f.read()
        
        return f'''
<Rules>
- We had a conversation about the topic.
- The conversation starts with the user answering the question, "what did you think of the TED Talk about ?"
- You reply shortly (2~3 sentences),
- Keep the English clear
<Role>
{role_prompt}
{script}
{conversation_example}
'''

    elif level == "C1" and purpose == "楽しく会話":
        with open("script/scr-freight.txt", "r", encoding="utf-8") as f:
            script = f.read()
        with open("sample-conversation/conv-freight.txt", "r", encoding="utf-8") as f:
            conversation_example = f.read()
        
        return f'''
<Rules>
- We had a conversation about the topic.
- The conversation starts with the user answering the question, "what did you think of the TED Talk about ?"
- You reply shortly (2~3 sentences),
- Keep the English clear
<Role>
{role_prompt}
{script}
{conversation_example}
'''

    elif level == "C1" and purpose == "英語力の向上":
        with open("script/scr-freight.txt", "r", encoding="utf-8") as f:
            script = f.read()
        with open("sample-conversation/conv-freight.txt", "r", encoding="utf-8") as f:
            conversation_example = f.read()
        
        return f'''
<Rules>
- We had a conversation about the topic.
- The conversation starts with the user answering the question, "what did you think of the TED Talk about ?"
- You reply shortly (2~3 sentences),
- Keep the English clear
<Role>
{role_prompt}
{script}
{conversation_example}
'''
# 説明テキストを読み込む関数
def load_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# JSON を読み込む関数
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# ================== 各ページ描画 ==================
def home_page():
    st.title("ホーム")
    st.session_state.username = st.text_input("名前を入力してください", placeholder="例）山田太郎")

    purpose = st.radio("ディスカッションの目的を選んでください", ["楽しく会話", "英語力の向上"])


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
    # 👇 選択された値を確認
    st.write("現在選択されている目的:", st.session_state.purpose)
    
    
    st.title(f"{st.session_state.level} レベル - TED動画")
    if st.session_state.level == "B2":
        st.video("https://www.youtube.com/watch?v=YXn-eNPzlo8")
    else:
        st.video("https://www.youtube.com/watch?v=1VA4rIkpSp8")

    col1, col2 = st.columns(2)
    with col1:
        st.button("戻る", on_click=lambda: (reset_chat(), go_to("home")))
    with col2:
        st.button("次へ", on_click=lambda: go_to("explanation"))


def explanation_page():
        # 👇 選択された値を確認
    st.write("現在選択されている目的:", st.session_state.purpose)
    
    st.title(f"{st.session_state.level} レベル - 解説")
    if st.session_state.level == "B2":
        # Step 1: 全文翻訳
        st.subheader("全文翻訳と解説")
        with st.expander("本文と翻訳を表示"):
            explanation_text = load_text("explanation-text/exp_dream.txt")
            st.write(explanation_text)

        # Step 2: 重要単語
        st.subheader("重要単語")
        vocab_data = load_json("explanation-text/vocab_dream.json")
        st.table(vocab_data)

        # Step 3: 重要フレーズ
        st.subheader("重要フレーズ")
        phrase_data = load_json("explanation-text/phrase_dream.json")
        st.table(phrase_data)

    else:
        # Step 1: 全文翻訳
        st.subheader("全文翻訳と解説")
        with st.expander("本文と翻訳を表示"):
            explanation_text = load_text("explanation-text/exp_freight.txt")
            st.write(explanation_text)

        # Step 2: 重要単語
        st.subheader("重要単語")
        vocab_data = load_json("explanation-text/vocab_freight.json")
        st.table(vocab_data)

        # Step 3: 重要フレーズ
        st.subheader("重要フレーズ")
        phrase_data = load_json("explanation-text/phrase_freight.json")
        st.table(phrase_data)

    col1, col2 = st.columns(2)
    
    with col1:
        st.button("戻る", on_click=lambda: go_to("video"))
    with col2:
        st.button("次へ", on_click=lambda: go_to("chat"))

jst = zoneinfo.ZoneInfo("Asia/Tokyo")

def add_message(role, content):
    message = {"role": role, "content": content}

    if role == "user":
        start  = st.session_state.get("chat_timer_start")
        if start:
            elapsed = datetime.now(jst) - start
            minutes, seconds = divmod(int(elapsed.total_seconds()), 60)
            message["delay"] = f"[{minutes}分{seconds}秒]"
            st.session_state.chat_timer_start = None
        else:
            message["delay"] = ""
    else:  # GPTの返答
        st.session_state.chat_timer_start = datetime.now(jst)
        message["delay"] = ""

    st.session_state.messages.append(message)

def chat_page():
    # チャットページに初めて入ったときだけ開始時間を記録
    if st.session_state.chat_start_time is None:
        st.session_state.chat_start_time = datetime.now()
    
    if "chat_timer_start" not in st.session_state:
        st.session_state.chat_timer_start = None

        
    st.write("現在選択されている目的:", st.session_state.purpose)
    st.title(f"{st.session_state.level} - {st.session_state.purpose}")
    api_key = st.secrets["API_KEY"]
    client = openai.OpenAI(api_key=api_key)

    # --- system プロンプトを毎回更新する版 ---
    if not st.session_state.messages:
        st.session_state.messages = [
            {"role": "system",
             "content": get_system_prompt(st.session_state.level, st.session_state.purpose)},
            {"role": "assistant", "content": "what did you think of the TED Talk about?"}
        ]
        if st.session_state.chat_timer_start is None:  #初回のみ
            st.session_state.chat_timer_start = datetime.now(jst)
    else:
        if st.session_state.messages[0]["role"] == "system":
            st.session_state.messages[0]["content"] = get_system_prompt(
                st.session_state.level, st.session_state.purpose
            )

    # 過去の会話を表示
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # ユーザー入力
    if prompt := st.chat_input("質問や感想を入力してください"):
        add_message("user", prompt)  #遅延付きで保存
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

        add_message("assistant", reply)  

    col1, col2 = st.columns(2)
    with col1:
        st.button("戻る", on_click=lambda: go_to("explanation"))
    with col2:
        def go_survey():
            # 1. チャット時間を計算
            start = st.session_state.chat_start_time
            if start:
                elapsed = datetime.now() - start
                minutes, seconds = divmod(int(elapsed.total_seconds()), 60)
                st.session_state.chat_duration = f"{minutes}分{seconds}秒"
    
            # 2. 会話内容をログに整形
            log_text = ""

            username = st.session_state.get("username", "名無し")
            jst = zoneinfo.ZoneInfo("Asia/Tokyo")
            now = datetime.now(jst)
            log_text += f"名前: {username}\n"
            log_text += f"保存日時: {now.strftime('%Y-%m-%d %H:%M:%S')}\n"


            log_text += f"\n"

            level = st.session_state.get("level", "未選択")
            purpose = st.session_state.get("purpose", "未選択")
            log_text += f"レベル: {level}\n"
            log_text += f"目的: {purpose}\n"
            log_text += f"\n"
            
            for m in st.session_state.messages:
                if m["role"] != "system":
                    prefix = "User" if m["role"] == "user" else "GPT"
                   
                    if m["role"] == "user":
                        delay = f" {m['delay']}" if m.get("delay") else ""
                    else:
                        delay = ""
                    log_text += f"{prefix}: {m['content']}{delay}\n"
    
            log_text += f"\n⏱ チャット滞在時間: {st.session_state.chat_duration}"
    
            # 3. GitHub に送信
            jst = zoneinfo.ZoneInfo("Asia/Tokyo")
            now = datetime.now(jst)
            filename = f"log/{st.session_state.username}_{now.strftime('%Y%m%d_%H%M%S')}.txt"
            response = push_to_github(filename, log_text)
    
            # 4. 成功/失敗を通知
            if response.status_code in [200, 201]:
                st.success(f"✅ {filename} をGitHubに保存しました！")
            else:
                st.error(f"❌ 送信失敗: {response.json()}")
    
            # 5. ページ遷移
            go_to("survey")

        st.button("次へ", on_click=go_survey)


def survey_page():
    st.title("アンケート")
    st.markdown("[Googleフォームはこちら](https://docs.google.com/forms/d/xxxxxx)")

    if st.session_state.messages:
        log_text = ""
        for m in st.session_state.messages:
            if m["role"] != "system":
                prefix = "User" if m["role"] == "user" else "GPT"
                log_text += f"{prefix}: {m['content']}\n"



    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.button("チャットに戻る", on_click=lambda: go_to("chat"))
    with col2:
        # ホームに戻る際にチャットをログをリセット
        st.button("ホームに戻る", on_click=lambda: (reset_chat(), go_to("home"))) 

# -------- ページ遷移 --------
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
