import streamlit as st
import openai
from datetime import datetime
import zoneinfo
from common import display_header, get_system_prompt, add_message, go_to, push_to_github

jst = zoneinfo.ZoneInfo("Asia/Tokyo")

# --------セッション状態の初期化 --------
if "chat_start_time" not in st.session_state:
    st.session_state.chat_start_time = None
if "chat_timer_start" not in st.session_state:
    st.session_state.chat_timer_start = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "input_counter" not in st.session_state:
    st.session_state.input_counter = 0
if "level" not in st.session_state:
    st.session_state.level = ""
if "purpose" not in st.session_state:
    st.session_state.purpose = "楽しく会話"
if "chat_duration" not in st.session_state:
    st.session_state.chat_duration = None
if "username" not in st.session_state:
    st.session_state.username = ""

# -------- ページコンテンツ --------
display_header()

# チャットページに初めて入ったときだけ開始時間を記録
if st.session_state.chat_start_time is None:
    st.session_state.chat_start_time = datetime.now()

st.title("ディスカッション")
st.caption(f"{st.session_state.level} - {st.session_state.purpose}")

st.warning("""
**注意事項**
- わからない箇所を質問したり、意見を述べたりしながら、ビデオの理解を深めることを目的としています。
- 英語で２回以上、好きなだけ会話文を送信してください。
- 不快に感じたり疲れた場合は、いつでも終了してください。
- 翻訳機能を使って内容を理解していただいても構いません。
""")       
    
with st.expander("チャット画面の見方"):
    col1, col2 = st.columns([0.5, 9.5])
    with col1:
        st.image("image/bot.png", width=30)
    with col2:
        st.markdown("チャットボット(会話相手)")
    
    col1, col2 = st.columns([0.5, 9.5])
    with col1:
        st.image("image/user.png", width=30)
    with col2:
        st.markdown("ユーザー(あなた)")
        
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

            # --- ユーザー発言に番号を付与 ---
            index = f"{m['index']}" if m.get("index") else ""

            if m["role"] == "user":
                delay = f" {m['delay']}" if m.get("delay") else ""
            else:
                delay = ""
            log_text += f"{prefix}: {m['content']}{delay}{index}\n"
            # log_text += f"{prefix}: {m['content']}{delay}\n"

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
    st.switch_page("pages/survey_enjoy.py")

# ボタンを配置
col1, col2 = st.columns([1, 1])

with col1:
    # 戻るボタン：チャットリセットしてホームに戻る
    if st.button("戻る", use_container_width=True):
        st.switch_page("pages/quiz.py")
with col2:
    # 次へボタン：クイズページに遷移
    if st.button("ディスカッションを終了する", use_container_width=True, type="primary"):
        # 5. ページ遷移
        go_survey() 