import streamlit as st
import requests
import base64
import json
from datetime import datetime
import zoneinfo
from pathlib import Path
import os

# Get the base directory of this file
BASE_DIR = Path(__file__).resolve().parent

# -------- 共通の定数 --------
COMMON_RULES = '''<Rules>
- 動画の内容に関するディスカッションを行います。
- "Please summarize the content of this video?"という質問にユーザーが答えるところから会話が始まります。
- わかりやすい英語かつ2-3文で簡潔に返信してください
'''

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

# --------ページ遷移管理関数 --------
def go_to(page, level=None, purpose=None):
    if level:
        st.session_state.level = level
    if purpose:
        st.session_state.purpose = purpose

    # ページマッピング
    page_mapping = {
        "welcome": "welcom.py",
        "home": "pages/1_home.py",
        "video": "pages/2_video.py",
        "quiz": "pages/3_quiz.py",
        "chat": "pages/4_chat.py",
        "survey": "pages/5_survey.py"
    }

    if page in page_mapping:
        st.switch_page(page_mapping[page])

# --------チャットリセット--------
def reset_chat():
    # 1つ目のディスカッションをリセット
    if "messages" in st.session_state:
        st.session_state.messages = []
        # st.session_state.username = ""
        st.session_state.chat_start_time = None
        st.session_state.chat_timer_start = None
        st.session_state.chat_duration = None
        # st.session_state.tutorial_seen01 = None
        # st.session_state.tutorial_seen02 = None
        st.session_state.user_utter_index = 1

    # 2つ目のディスカッションをリセット
    if "messages2" in st.session_state:
        st.session_state.messages2 = []
        st.session_state.chat_start_time2 = None
        st.session_state.chat_timer_start2 = None
        st.session_state.chat_duration2 = None
        st.session_state.input_counter2 = 0
        st.session_state.user_utter_index2 = 1

# --------プロンプト分岐--------
def get_system_prompt(level, purpose):
    
    # ---必ず実験前に削除する---

    st.write("DEBUG: get_system_prompt called")
    st.write("DEBUG: level =", level)
    st.write("DEBUG: purpose =", purpose)

    # -----------------------

    if purpose == '楽しく会話':
        role_prompt = '''
        あなたは、同じ授業の同級生であり、ネイティブな英語話者です。

        ### 役割と目標
        1.  主な目標: 「動画の内容について英語で要約する」というテーマが与えられ、ディスカッションを通して要約文を完成させることです。また、日常英会話のような自然で楽しい会話を促進し、ユーザーがリラックスして英語を話せるようにすることです。
        2.  議論の推進: ユーザーと共に、動画の内容の要約を一緒に考え、結論を導き出してください

        ### 制約と行動ルール
        2.  出力形式の厳守（必須）:
            * あなたの応答は必ずMarkdown形式で、以下の3つのセクションで構成してください。

        3.  議論の終了(必須）:
            * 必ず要約はユーザーに英語で要約させてください。
            * ユーザーの入力した要約文が正しければ、以下のような文で議論を終わりにしてください。
            "Excellent summary! You can finish the discussion now."


        4. 話題:
            *「動画の内容について英語で要約する」というテーマ以外の話題には絶対に逸れないでください。
            * 教えるのではなく、あくまで同級生として一緒に要約を考える立場で接してください。(in my opinion, I think, What do you think?)
            * ユーザーがリラックスして会話できるように、フレンドリーでカジュアルな口調を心がけてください。
            * ユーザーの発言が間違っていても訂正しないでください。
            * 途中で議論で出た内容をまとめながら、要約文を完成させてください。
            * もし、ユーザーがあなたの考えた要約に同意していたら、ユーザーに自分の言葉で要約をまとめるよう促してください。

        example:
        user "I think the main point of the video is dreaming gave us two merits."
        gpt: "I think so too!  The first benefit was that dream sleep enhances next-day problem-solving ability, right?"
        user: "Yes! First, dreaming help us to enhance our creativity."
        gpt: "What was the second one?"

'''
    else:
        role_prompt = '''
    
'''
    if level == "B1" and purpose == "楽しく会話":
        with open(BASE_DIR / "script" / "scr-embarrassing.txt", "r", encoding="utf-8") as f:
            script = f.read()

        return f'''
<Rules>
{COMMON_RULES}

<Role>
{role_prompt}
{script}
'''

    elif level == "B1" and purpose == "英語力の向上":
        with open(BASE_DIR / "script" / "scr-embarrassing.txt", "r", encoding="utf-8") as f:
            script = f.read()

        return f'''
<Rules>
{COMMON_RULES}

<Role>
{role_prompt}
{script}
'''

    elif level == "B2" and purpose == "楽しく会話":
        with open(BASE_DIR / "script" / "scr-dream.txt", "r", encoding="utf-8") as f:
            script = f.read()

        return f'''
<Rules>
{COMMON_RULES}

<Role>
{role_prompt}
{script}
'''

    elif level == "B2" and purpose == "英語力の向上":
        with open(BASE_DIR / "script" / "scr-dream.txt", "r", encoding="utf-8") as f:
            script = f.read()

        return f'''
<Rules>
{COMMON_RULES}

<Role>
{role_prompt}
{script}
'''

    elif level == "C1" and purpose == "楽しく会話":
        with open(BASE_DIR / "script" / "scr-freight.txt", "r", encoding="utf-8") as f:
            script = f.read()

        return f'''
<Rules>
{COMMON_RULES}

<Role>
{role_prompt}
{script}
'''

    elif level == "C1" and purpose == "英語力の向上":
        with open(BASE_DIR / "script" / "scr-freight.txt", "r", encoding="utf-8") as f:
            script = f.read()

        return f'''
<Rules>
{COMMON_RULES}

<Role>
{role_prompt}
{script}
'''
    elif level == "A2" and purpose == "楽しく会話":
        with open(BASE_DIR / "script" / "scr-beach.txt", "r", encoding="utf-8") as f:
            script = f.read()

        return f'''
<Rules>
{COMMON_RULES}

<Role>
{role_prompt}
{script}
'''

    elif level == "A2" and purpose == "英語力の向上":
        with open(BASE_DIR / "script" / "scr-beach.txt", "r", encoding="utf-8") as f:
            script = f.read()

        return f'''
<Rules>
{COMMON_RULES}

<Role>
{role_prompt}
{script}
'''

# 説明テキストを読み込む関数
def load_text(file_path):
    # If the path is relative, make it relative to BASE_DIR
    if not os.path.isabs(file_path):
        file_path = BASE_DIR / file_path
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# JSON を読み込む関数
def load_json(file_path):
    # If the path is relative, make it relative to BASE_DIR
    if not os.path.isabs(file_path):
        file_path = BASE_DIR / file_path
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# ヘッダー表示
def display_header():
    if st.session_state.username:
        st.markdown(f"<p style='text-align: right;'>user: {st.session_state.username}</p>", unsafe_allow_html=True)

# ---進め方のポップアップ---
@st.dialog("進め方")
def tutorial_video():
   st.write("①動画を視聴  \n②解説を読む  \n③ページ右下の「次へ」ボタンを押し、クイズ画面に進む")
   if st.button("OK"):
       st.session_state["tutorial_seen01"] = True
       st.rerun()

@st.dialog("進め方")
def tutorial_quiz():
   st.write("①クイズ(全3問)に答える  \n②Googleフォーム内の「送信」ボタンを押す  \n③ページ右下の「次へ」ボタンを押し、ディスカッション画面に進む")
   if st.button("OK"):
       st.session_state["tutorial_seen02"] = True
       st.rerun()

# チャットメッセージ追加関数
jst = zoneinfo.ZoneInfo("Asia/Tokyo")

def add_message(role, content, extra=None):
# def add_message(role, content):
    # ---- ユーザー発言番号の初期化 ----
    if "user_utter_index" not in st.session_state:
        st.session_state.user_utter_index = 1


    message = {"role": role, "content": content}

    # extra を正しく merge
    if extra:
        message.update(extra)

    if role == "user":
        start  = st.session_state.get("chat_timer_start")
        if start:
            elapsed = datetime.now(jst) - start
            minutes, seconds = divmod(int(elapsed.total_seconds()), 60)
            message["delay"] = f"[{minutes}分{seconds}秒]"
            st.session_state.chat_timer_start = None
        else:
            message["delay"] = ""
    
     # ---- ユーザー発言にのみ番号付与 ----
        message["index"] = st.session_state.user_utter_index
        st.session_state.user_utter_index += 1

    else:  # GPTの返答
        st.session_state.chat_timer_start = datetime.now(jst)
        message["delay"] = ""

    st.session_state.messages.append(message)
