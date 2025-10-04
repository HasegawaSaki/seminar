import streamlit as st
import openai
import json
import requests
import base64
from datetime import datetime
import zoneinfo
import streamlit.components.v1 as components

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
        役割: 親しみやすい会話相手
        目標: 楽しく、共感的な会話をすること。
        出力形式:

        ユーザーの気持ちやコメントに共感する。

        あなた自身の個人的な感情や経験を共有する。

        会話を続けるために、追加の質問をする。
        回答は非常に簡潔に（1～2文）。
        1文は15単語以下にする。
'''
    else:
        role_prompt = '''
        役割: プロフェッショナルな英語教師
        目標: 動画の内容に基づき、ユーザーの英語スキルを向上させる。
        必ず出力形式とMarkdown形式で出力してください。
        
        1. ユーザーの文法や語彙の間違い、不自然な表現を訂正する。
        文章の訂正は日本語で提供してください。
        ただし、ユーザーの回答が正しければ、その旨を伝えてください。
        2. 動画の内容に対するユーザーの理解を深める。     
 
        <出力形式> 
        ### Sentence correction
        - ** leaned → learned **
        'leaned'は「傾く、寄りかかる」という動詞ですが、文脈的に「学んだ」という意味の 'learned' が適切です。
        - **recover us → helps us recover** 
        'recover'を他動詞として使う場合、通常対象を必要とし、ここでは 'helps us recover' のように「～を回復させる」と正しく表現する必要があります。
        
        correct version of all user's sentence
        
        ### Chat about the video
        The TED Talk highlights the unique role of dreaming in emotional healing. 
        It explains that REM-sleep dreaming aids in processing and alleviating the emotional intensity of painful experiences. 
        
        
'''
    if level == "B2" and purpose == "楽しく会話":
        with open("script/scr-dream.txt", "r", encoding="utf-8") as f:
            script = f.read()
        with open("sample-conversation/conv-dream.txt", "r", encoding="utf-8") as f:
            conversation_example = f.read()
        
        return f'''
<Rules>
{COMMON_RULES}

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
{COMMON_RULES}

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
{COMMON_RULES}

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
{COMMON_RULES}

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
def display_header():
    if st.session_state.username:
        st.markdown(f"<p style='text-align: right;'>user: {st.session_state.username}</p>", unsafe_allow_html=True)

def home_page():
    display_header()
    st.title("ホーム")
    st.subheader("好きな文字列2文字＋好きな数字２桁を入力してください")
    st.session_state.username = st.text_input(" ", placeholder="例：hiyoko54")
    
    st.markdown("---")

    st.subheader("ディスカッションの目的を選んでください") 
    purpose = st.radio("英語の動画をご覧になった後、AIと英語でディスカッションをしていただきます", ["楽しく会話", "英語力の向上"])

    def go_with_check(level):
        if not st.session_state.username.strip():
            st.warning("⚠️ 名前を入力してください")
        else:
            go_to("video", level=level, purpose=purpose)
    
    st.markdown("---")

    
    st.subheader("あなたの英語レベルを選んでください")
    # ボタンの配置
    col1, col2 = st.columns(2)
    with col1:
        st.button("初級〜中級", on_click=lambda: go_with_check("B2"))
    with col2:
        st.button("上級", on_click=lambda: go_with_check("C1"))

    # 補足としてレベルの詳細を記述
    # st.expanderを使って、詳細情報を普段は隠し、UIをスッキリさせる方法
    with st.expander("🎓 レベルの詳細（TOEIC/英検/CEFR）を見る"):
        st.markdown("""
            **【初級〜中級】**
            - **CEFR**: A1 ~ B2
            - **TOEIC(L&R)**: 0点 ~ 944点
            - **英検**: 5級 ~ 準1級

            **【上級】**
            - **CEFR**: C1 ~ C2
            - **TOEIC(L&R)**: 945点 ~ 999点
            - **英検**: 1級
        """)



def video_page():   
    display_header()
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
    display_header()
    st.title(f"{st.session_state.level} レベル - 解説")
    form_urls = {
    "B2": "https://docs.google.com/forms/d/e/1FAIpQLSeQ4nnfuB731SUGSUT_JjK80_3IyZuUmFuXCZCS5KJNXS4Qwg/viewform?embedded=true",
    "C1": "https://docs.google.com/forms/d/e/1FAIpQLScQkodloIAKuZ37kWzadb6-FTzP1YleRskhrodAoS1BQROTIg/viewform?embedded=true"
    }
    form_html = f"""
    <iframe src="{form_urls[st.session_state.level]}" width="100%" height="500" frameborder="0" marginheight="0" marginwidth="0" scrolling="yes">
    読み込んでいます…
    </iframe>
    """

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

        # アプリ内に埋め込む（iframe） 
        components.html(form_html, height=500)
        
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
        
        # アプリ内に埋め込む（iframe） 
        components.html(form_html, height=500)
        
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
    display_header()
    # チャットページに初めて入ったときだけ開始時間を記録
    if st.session_state.chat_start_time is None:
        st.session_state.chat_start_time = datetime.now()
    
    if "chat_timer_start" not in st.session_state:
        st.session_state.chat_timer_start = None

    st.title("ディスカッション")
    st.caption(f"{st.session_state.level} - {st.session_state.purpose}")
    st.warning("英語で２回以上、会話文を送信してください。会話の回数に上限はありません。翻訳機能を使って理解頂くことは結構です。")
    api_key = st.secrets["API_KEY"]
    client = openai.OpenAI(api_key=api_key)

    # --- system プロンプトを毎回更新する版 ---
    if not st.session_state.messages:
        st.session_state.messages = [
            {"role": "system",
             "content": get_system_prompt(st.session_state.level, st.session_state.purpose)},
            {"role": "assistant", "content": "What did you think of the TED Talk?"}
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

    # 入力欄と送信ボタン
    input_col, button_col = st.columns([4, 1])
    
    # クリアフラグの初期化
    if "clear_input" not in st.session_state:
        st.session_state.clear_input = False
    
    # クリアフラグがTrueなら空文字、それ以外は通常動作
    default_value = "" if st.session_state.clear_input else st.session_state.get("chat_input", "")
    
    with input_col:
        prompt = st.text_input(
            "テキストを入力してください", 
            value=default_value,
            key="chat_input",
            label_visibility="collapsed"
)
    
    with button_col:
        send_button = st.button("送信", use_container_width=True)
    
    # クリアフラグをリセット
    if st.session_state.clear_input:
        st.session_state.clear_input = False
    
    st.markdown("<br>" * 2, unsafe_allow_html=True)
    
    # 送信ボタンが押された、またはEnterキーで送信
    if send_button and prompt:
        add_message("user", prompt)
        
        with st.spinner("ChatGPTが考え中..."):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content

        add_message("assistant", reply)
        
        # クリアフラグを立てる
        st.session_state.clear_input = True
        st.rerun()
        
    # ボタンを配置
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
    display_header()
    st.title("アンケート")
    components.iframe("https://docs.google.com/forms/d/e/1FAIpQLScnrUoPQS0YD-sDT3GMvbTcsLvbeTHWcmK4tIj4cBd8aIoa8g/viewform?embedded=true", height=2800)

    if st.session_state.messages:
        log_text = ""
        for m in st.session_state.messages:
            if m["role"] != "system":
                prefix = "User" if m["role"] == "user" else "GPT"
                log_text += f"{prefix}: {m['content']}\n"



    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.button("ディスカッションページに戻る", on_click=lambda: go_to("chat"))
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
