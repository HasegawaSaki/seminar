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
    st.session_state.page = "welcome"
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
if "show_warning" not in st.session_state:
   st.session_state.show_warning = False

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
        st.session_state.tutorial_seen01 = None
        st.session_state.tutorial_seen02 = None
        
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
        ###  Language Feedback and Correction
        (訂正は必ず日本語でしてください。
        ユーザーの発言が正しくても、このセクションは必ず含めてください。
        ユーザーの英文が完璧に場合は「文法・語彙の誤りはありませんでした！素晴らしいです。」などと記述してください。）

        -   **誤り箇所 $\rightarrow$ 正しい表現 / 不自然な表現 $\rightarrow$ より自然な表現**
            'leaned' は「傾く、寄りかかる」という意味で、ここでは文脈的に「学んだ」という意味の 'learned' が適切です。

        -   **recover us $\rightarrow$ helps us recover**
            'recover' を他動詞として使う場合、通常対象を必要とし、ここでは 'helps us recover' のように「～を回復させる」と正しく表現する必要があります。

        **文章全体の訂正バージョン:**
        (Corrected version of all user's sentence)
        [ここに、ユーザーの文章を修正した、自然で正確な英文全体を記述してください。]
        ***

        ###  Discussion About The Movie
        (ここでは英語のみを使用してください。)
        [フィードバック（例: That's a great summary!）と、要約を導き出すための質問をしてください。]
        
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

# ---進め方のポップアップ(ページ遷移後のスクロールバーの位置の調整が難しい(ホームから移動したらいきなりページ下部の解説画面が表示されたりする)ので、ポップアップで手順がわかったほうがいいかも!?邪魔そうだったら消します)---
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


def welcome_page():
    # カスタムCSS
    st.markdown("""
    <style>
    .welcome-header {
        text-align: center;
        padding: 2rem 0;
        background: #FB323B;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .welcome-title {
        color: white;
        font-size: 3em;
        font-weight: bold;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    .welcome-subtitle {
        color: #f0f0f0;
        font-size: 1.5em;
        margin-top: 0.5rem;
    }
    .welcome-description {
        text-align: center;
        font-size: 1.3em;
        margin: 2rem 0;
        line-height: 1.6;
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        margin-bottom: 1rem;
        border-left: 4px solid #FB323B;
        transition: transform 0.2s;
    }
    .feature-card:hover {
        transform: translateX(5px);
    }
    .feature-icon {
        font-size: 2em;
        margin-right: 0.5rem;
    }
    .feature-title {
        font-size: 1.3em;
        font-weight: bold;
        color: #333;
        margin-bottom: 0.5rem;
    }
    .feature-text {
        color: #666;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

    # ヘッダー
    st.markdown("""
    <div class='welcome-header'>
        <h1 class='welcome-title'>AI English Learning Tool</h1>
        <p class='welcome-subtitle'>TED動画でディスカッション</p>
    </div>
    """, unsafe_allow_html=True)

    # 説明文
    st.markdown("""
    <div class='welcome-description'>
        TED動画を視聴してAIとのディスカッションを<br>
        することにより英語学習をサポートします。
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 機能紹介
    st.markdown("""
    <div class='feature-card'>
        <div><span class='feature-icon'>📺</span><span class='feature-title'>TED動画の視聴</span></div>
        <div class='feature-text'>レベル別に厳選されたTED Talkを視聴できます</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='feature-card'>
        <div><span class='feature-icon'>📖</span><span class='feature-title'>動画の解説</span></div>
        <div class='feature-text'>重要単語やフレーズの学習、全文翻訳で内容理解をサポート</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='feature-card'>
        <div><span class='feature-icon'>💬</span><span class='feature-title'>AIとディスカッション</span></div>
        <div class='feature-text'>動画の内容について英語で会話<br>楽しく会話するモードと英語力向上モードを選択可能</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>" * 2, unsafe_allow_html=True)

    # スタートボタンを中央に配置
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.button("スタート", on_click=lambda: go_to("home"), use_container_width=True, type="primary")


def home_page():
    display_header()
    st.title("ホーム")
    st.subheader("指定のユーザーネームをご入力ください")
    
    st.session_state.username = st.text_input(" ", placeholder="例：A1014")
    
    st.markdown("---")

    st.subheader("学習したいディスカッションのタイプを選んでください(指定がある場合は指定のタイプを選んでください)") 
    purpose = st.radio("英語の動画をご覧になった後、AIと英語でディスカッションをしていただきます", ["楽しく会話", "英語力の向上"])

    def go_with_check(level):
        if not st.session_state.username.strip():
            st.session_state.show_warning = True
        else:
            st.session_state.show_warning = False
            go_to("video", level=level, purpose=purpose)
    
    st.markdown("---")

    if st.session_state.show_warning:
        st.warning("⚠️画面上部にあるフォームにユーザーネームを入力してください。")
        
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

    st.markdown("---")
    st.button("戻る", on_click=lambda: go_to("welcome"))


def video_page():   
    display_header()

    if "tutorial_seen01" not in st.session_state:
       st.session_state["tutorial_seen01"] = False
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
    

    col1, col2 = st.columns(2)
    with col1:
        st.button("戻る", on_click=lambda: (reset_chat(), go_to("home")))
    with col2:
        st.button("次へ", on_click=lambda: go_to("explanation"))



def explanation_page():
    display_header()
    if "tutorial_seen02" not in st.session_state:
        st.session_state["tutorial_seen02"] = False
    if not st.session_state["tutorial_seen02"]:
        tutorial_quiz()
    st.title(f"{st.session_state.level} レベル - クイズ")
    form_urls = {
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
        
    col1, col2 = st.columns(2)
    
    with col1:
        st.button("戻る", on_click=lambda: go_to("video"))
    with col2:
        st.button("次へ(ディスカッションに移動する)", on_click=lambda: go_to("chat"))

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
    st.warning("英語で２回以上、会話文を送信してください。チャットは好きなだけ続けていただいて構いません。  \nもし不快に感じたり、疲れた場合は、ご自身の判断でいつでも終了してください。翻訳機能を使って内容を理解していただいても構いません。")
    api_key = st.secrets["API_KEY"]
    client = openai.OpenAI(api_key=api_key)

    # --- system プロンプトを毎回更新する版 ---
    if not st.session_state.messages:
        st.session_state.messages = [
            {"role": "system",
             "content": get_system_prompt(st.session_state.level, st.session_state.purpose)},
            {"role": "assistant", "content": "Please summarize the content of this video?"}
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
    
    if "input_counter" not in st.session_state:
        st.session_state.input_counter = 0

    with input_col:
        prompt = st.text_input(
            "テキストを入力してください",
            value="",
            key=f"chat_input_{st.session_state.input_counter}",
            label_visibility="collapsed"
        )

    with button_col:
        send_button = st.button("送信", use_container_width=True)

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
        
        st.session_state.input_counter += 1
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

        st.button("ディスカッションを終了する", on_click=go_survey)
        
def survey_page():
    display_header()
    st.title("アンケート")
    if st.session_state.level == "B2":
        components.iframe("https://docs.google.com/forms/d/e/1FAIpQLScnrUoPQS0YD-sDT3GMvbTcsLvbeTHWcmK4tIj4cBd8aIoa8g/viewform?embedded=true", height=4500)
    else:
        components.iframe("https://docs.google.com/forms/d/e/1FAIpQLSfrwEok1A49dAboYeYTpbhq4XZlX7mRzdVu8W2L2BRKSttxmA/viewform?embedded=true", height=4500)
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
if st.session_state.page == "welcome":
    welcome_page()
elif st.session_state.page == "home":
    home_page()
elif st.session_state.page == "video":
    video_page()
elif st.session_state.page == "explanation":
    explanation_page()
elif st.session_state.page == "chat":
    chat_page()
elif st.session_state.page == "survey":
    survey_page()
