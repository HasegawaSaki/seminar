import streamlit as st
import openai
import requests
import base64
import datetime
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
        st.session_state.chat_duration = None
        
# --------プロンプト分岐--------
def get_system_prompt(level, purpose):
    if purpose == '楽しく会話':
        role_prompt = "The conversation is casual. Shares personal feelings and experiences. if the user asks questions, answer them so briefly(1-2sentense). The goal is to have fun and enjoy the conversation. please emphathize with the user's comments,and sometimes offer your own opininon as if your were a friend."
    else:
        role_prompt = "You are English teacher. The conversation is intelligent and easy to understand. The goal is to help the user improve their English skills and deepen their understanding of the video's content. please correct the user's grammar and vocabulary mistakes, and provide explanations for any difficult words or phrases used in the video."
    
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
            st.write("""
            **Well, we dream for at least several different reasons.**  
            さて、私たちは少なくともいくつかの異なる理由で夢を見ています。
    
            **One key benefit is creativity.**  
            主な利点の一つは創造性です。
    
            **Sleep, including dream sleep, is associated with an enhanced ability to solve next-day problems.**  
            夢を見る睡眠を含む睡眠は、翌日の問題解決能力の向上と関連しています。
    
            **It's almost as though we go to sleep with the pieces of the jigsaw, but we wake up with the puzzle complete.**  
            まるで私たちがジグソーパズルのピースを持って眠り、目覚めたときにはパズル全体が完成しているかのようです。
    
            **The second benefit of REM-sleep dreaming is emotional first aid.**  
            REM睡眠中の夢のもう一つの利点は感情的な応急処置です。
    
            **REM sleep takes the painful sting out of difficult emotional experiences so that when we come back the next day, we feel better about those painful events.**  
            REM睡眠はつらい感情的経験の痛みを和らげるため、翌日それらの出来事について前よりも気分が良くなるのです。
    
            **You can almost think of dreaming as a form of overnight therapy.**  
            夢を見ることは、一晩で行われるセラピーのようなものだと考えられるでしょう。
    
            **It's not time that heals all wounds, but it's time during dream sleep that provides emotional convalescence.**  
            すべての傷を癒すのは単なる時間ではなく、夢の中で眠っているその時間こそが感情の回復をもたらすのです。
    
            **Now, it's not just that you dream. It's also what you dream about that seems to make a difference.**  
            さて、夢を見ること自体だけでなく、「何について夢を見るか」も違いを生んでいるようです。
    
            **Scientists have discovered that after learning a virtual maze, for example, those individuals who slept but critically also dreamed about the maze were the only ones who ended up being better at navigating the maze when they woke up.**  
            例えば、仮想迷路の操作を学んだ後で、眠った人の中でも特にその迷路について夢を見た人だけが、目覚めたときにより上手に迷路を進めることができると科学者たちは発見しました。
    
            **And this same principle is true for our mental health.**  
            そして、この同じ原則は私たちの心の健康にも当てはまります。
    
            **For example, people going through a difficult or traumatic experience such as a divorce, and who are dreaming about that event, go on to gain resolution to their depression relative to those who were dreaming but not dreaming about the events themselves.**  
            例えば、離婚のような困難やトラウマとなる経験をしている人で、その出来事について夢を見る人は、そうでない夢を見る人と比べ、うつ状態の解消に至ることがより多いのです。
    
            **All of which means that sleep and the very act of dreaming itself appears to be an essential ingredient to so much of our waking lives.**  
            これら全ては、睡眠および夢を見るという行為そのものが、私たちの起きている時間の生活にとって不可欠な要素であることを意味しています。
    
            **We dream, therefore we are.**  
            私たちは夢を見る。ゆえに私たちは存在する。
            """)
    
        # Step 2: 単語リスト
        st.subheader("重要単語")
        vocab_data = [
            {"英単語": "creativity", "意味": "創造性", "品詞": "名詞", "例文": "Creativity is important for artists and engineers."},
            {"英単語": "associated", "意味": "関連した、関係した", "品詞": "形容詞", "例文": "Exercise is associated with good health."},
            {"英単語": "enhanced", "意味": "強化された、より高められた", "品詞": "形容詞", "例文": "The new phone has enhanced features."},
            {"英単語": "jigsaw", "意味": "ジグソーパズル", "品詞": "名詞", "例文": "He bought a difficult jigsaw for his daughter."},
            {"英単語": "REM-sleep", "意味": "レム睡眠（夢の多い深い睡眠）", "品詞": "名詞", "例文": "REM-sleep is important for our mental health."},
            {"英単語": "sting", "意味": "（感情的な）痛み、ひりひりする感覚", "品詞": "名詞", "例文": "The sting of his words lasted for days."},
            {"英単語": "therapy", "意味": "治療、セラピー", "品詞": "名詞", "例文": "Music can be a kind of therapy for stress."},
            {"英単語": "convalescence", "意味": "回復期間", "品詞": "名詞", "例文": "He needed a week of convalescence after surgery."},
            {"英単語": "virtual", "意味": "仮想の、バーチャルの", "品詞": "形容詞", "例文": "I enjoyed the virtual museum tour on my computer."},
            {"英単語": "traumatic", "意味": "トラウマになる、心的外傷の", "品詞": "形容詞", "例文": "The earthquake was a traumatic experience for many residents."}
        ]
        st.table(vocab_data)
    
        # Step 3: フレーズリスト
        st.subheader("重要フレーズ")
        phrase_data = [
            {"英語フレーズ": "be associated with A", "意味": "Aと関連している", "例文": "Heart disease is associated with unhealthy eating habits."},
            {"英語フレーズ": "as though S V", "意味": "まるでSがVするかのように", "例文": "She talks as though she knows everything."},
            {"英語フレーズ": "take the sting out of A", "意味": "Aの痛み・つらさを和らげる", "例文": "Laughter can take the sting out of difficult situations."},
            {"英語フレーズ": "a form of A", "意味": "Aの一形態", "例文": "Meditation is a form of relaxation."},
            {"英語フレーズ": "an essential ingredient to A", "意味": "Aに不可欠な要素", "例文": "Trust is an essential ingredient to a happy relationship."}
        ]
        st.table(phrase_data)

    else:
        st.markdown("C1解説準備中")

    col1, col2 = st.columns(2)
    
    with col1:
        st.button("戻る", on_click=lambda: go_to("video"))
    with col2:
        st.button("次へ", on_click=lambda: go_to("chat"))


def chat_page():
    # チャットページに初めて入ったときだけ開始時間を記録
    if st.session_state.chat_start_time is None:
        st.session_state.chat_start_time = datetime.now()
        
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
        def go_survey():
            start = st.session_state.chat_start_time
            if start:
                elapsed = datetime.now() - start
                minutes, seconds = divmod(int(elapsed.total_seconds()), 60)
                st.session_state.chat_duration = f"{minutes}分{seconds}秒"
            go_to("survey")

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

        # チャット滞在時間を追加
        if st.session_state.chat_duration:
            log_text += f"\n⏱ チャット滞在時間: {st.session_state.chat_duration}\n"

        if st.button("🚀 ログを送信（GitHubに保存）"):
            jst = zoneinfo.ZoneInfo("Asia/Tokyo")
            now = datetime.now(jst)
            filename = f"log/{st.session_state.username}_{now.strftime('%Y%m%d_%H%M%S')}.txt"
            response = push_to_github(filename, log_text)
            if response.status_code in [200, 201]:
                st.success(f"✅ {filename} をGitHubに保存しました！")
            else:
                st.error(f"❌ 送信失敗: {response.json()}")

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
