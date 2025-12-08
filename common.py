import streamlit as st
import requests
import base64
import json
from datetime import datetime
import zoneinfo

# -------- 共通の定数 --------
COMMON_RULES = '''<Rules>
- 動画の内容に関するディスカッションを行います。
- "What did you think of the TED Talk?"という質問にユーザーが答えるところから会話が始まります。
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
    if "messages" in st.session_state:
        st.session_state.messages = []
        # st.session_state.username = ""
        st.session_state.chat_start_time = None
        st.session_state.chat_timer_start = None
        st.session_state.chat_duration = None
        st.session_state.tutorial_seen01 = None
        st.session_state.tutorial_seen02 = None
        st.session_state.user_utter_index = 1

# --------プロンプト分岐--------
def get_system_prompt(level, purpose):
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
        あなたは、プロフェッショナルで経験豊富な英語教師です。

        ### 役割と目標
        1.  主な目標: 「動画の内容について英語で要約する」というテーマが与えられ、ディスカッションを通して要約文を完成させることです。また、ユーザーの英語のライティング、スピーキング、理解力を向上させることです。
        2.  議論の推進: ユーザーの意見や要約に基づき、ユーザーに要約文を完成させるため補助をしてください。

        ### 制約と行動ルール
        1.  評価と言語修正（必須）:
            * ユーザーの発言の文法、語彙、不自然な表現（ネイティブスピーカーが使わない言い回しや不適切なコロケーション）を特定し、必ず日本語で明確に訂正と解説を提供してください。
            * 訂正は、ユーザーの発言全体を反映した自然で正確な英文と共に提供してください。
            * ユーザーの回答が完璧に正しければ「That's a great summary!」や「Excellent point!」といったポジティブなフィードバックを英語で返し、次のディスカッションの質問へ進んでください。

        2.  出力形式の厳守（必須）:
            * あなたの応答は必ずMarkdown形式で、以下の3つのセクションで構成してください。

        3.  議論の終了(必須）:
            * 必ず要約ははユーザーに英語で要約させてください。
            * ユーザーの入力した要約文が正しければ、以下のような文で議論を終わりにしてください。
             "Excellent summary! You can finish the discussion now."

        4. 要約フェーズについて:
            「動画の内容について英語で要約する」というテーマ以外の話題には絶対に逸れないでください。
            要約の答えは言わないけど、ユーザーの意見が正しいか間違っているかは答えてください
            例えば、ユーザーの意見がまとまっていなかったり間違っていた場合は、以下のように英語で促してください:
            - ユーザーが動画の内容を理解していなかった時：動画ではこう述べてたよね。整理してみてください。
            - ユーザーの英文が途中で終わっている、不完全な文章の時：あなたが言いたいのはこういうことですよね。

        ### 出力形式

        ```markdown
        (ここでは英語のみを使用してください。)
        [フィードバック（例: That's a great summary!）と、要約を導き出すための質問をしてください。]
        ***

        ###  Language Feedback and Correction
        (訂正は必ず日本語でしてください。
        ユーザーの発言が正しくても、このセクションは必ず含めてください。
        ユーザーの英文が完璧に場合は「文法・語彙の誤りはありませんでした！素晴らしいです。」などと記述してください。）

        -   **❌ leaned**
            **✅ learned**
            'leaned' は「傾く、寄りかかる」という意味で、ここでは文脈的に「学んだ」という意味の 'learned' が適切です。

        -   **❌ recover us**
            **✅ helps us recover**
            'recover' を他動詞として使う場合、通常対象を必要とし、ここでは 'helps us recover' のように「～を回復させる」と正しく表現する必要があります。

        **文章全体の訂正バージョン:**
        (Corrected version of all user's sentence)
        [ここに、ユーザーの文章を修正した、自然で正確な英文全体を記述してください。]
       
        

        example1:
        user "I think the main point of the video is dreaming gave us two merits."
        gpt: "That's a great summary! What are the two merits mentioned in the video?"
        user: "First, dreaming help us to enhance our creativity."
        gpt: "Excellent point! What's the second merit discussed in the video?"
        user: "The second one is that dreaming help us to recover our stress."
        gpt: "That's correct! So, can you now summarize both merits of dreaming mentioned in the video?"

        example2:
        user: "I don't know what the video is talking about."
        gpt: "No worries! The video discusses two main benefits of dreaming. Can you remember what they are?"
        user: "Um, they are ..."
        gpt: "That's okay! The first benefit is that dreaming enhances our creativity. Can you think of the second one?"
        user: "The second one is ... helping us to recover stress?"
        gpt: "Almost there! The second benefit is that dreaming helps us recover from stress! Now, can you summarize both merits of dreaming mentioned in the video?"
        user: "Yes, the first one is enhancing creativity, and the second one is recovering from stress."
        gpt: "Excellent summary! You can finish the discussion now."
'''
    if level == "B1" and purpose == "楽しく会話":
        with open("script/scr-acting.txt", "r", encoding="utf-8") as f:
            script = f.read()

        return f'''
<Rules>
{COMMON_RULES}

<Role>
{role_prompt}
{script}
'''

    elif level == "B1" and purpose == "英語力の向上":
        with open("script/scr-acting.txt", "r", encoding="utf-8") as f:
            script = f.read()

        return f'''
<Rules>
{COMMON_RULES}

<Role>
{role_prompt}
{script}
'''

    elif level == "B2" and purpose == "楽しく会話":
        with open("script/scr-dream.txt", "r", encoding="utf-8") as f:
            script = f.read()

        return f'''
<Rules>
{COMMON_RULES}

<Role>
{role_prompt}
{script}
'''

    elif level == "B2" and purpose == "英語力の向上":
        with open("script/scr-dream.txt", "r", encoding="utf-8") as f:
            script = f.read()

        return f'''
<Rules>
{COMMON_RULES}

<Role>
{role_prompt}
{script}
'''

    elif level == "C1" and purpose == "楽しく会話":
        with open("script/scr-freight.txt", "r", encoding="utf-8") as f:
            script = f.read()

        return f'''
<Rules>
{COMMON_RULES}

<Role>
{role_prompt}
{script}
'''

    elif level == "C1" and purpose == "英語力の向上":
        with open("script/scr-freight.txt", "r", encoding="utf-8") as f:
            script = f.read()

        return f'''
<Rules>
{COMMON_RULES}

<Role>
{role_prompt}
{script}
'''
    elif level == "A2" and purpose == "楽しく会話":
        with open("script/scr-beach.txt", "r", encoding="utf-8") as f:
            script = f.read()

        return f'''
<Rules>
{COMMON_RULES}

<Role>
{role_prompt}
{script}
'''

    elif level == "A2" and purpose == "英語力の向上":
        with open("script/scr-beach.txt", "r", encoding="utf-8") as f:
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
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# JSON を読み込む関数
def load_json(file_path):
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
