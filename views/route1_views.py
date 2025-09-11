import streamlit as st
import openai
import requests
import base64
import datetime
from datetime import datetime
import zoneinfo
from utils import go_to, go_to_and_clear_chat

def render_video():
    st.title("TED動画を見る")
    st.video("https://www.youtube.com/watch?v=YXn-eNPzlo8")
    col1, col2 = st.columns(2)
    with col1:
        st.button("戻る", on_click=lambda: go_to("home"))
    with col2:
        st.button("次へ", on_click=lambda: go_to("explanation1"))

def render_explanation():
    # ---------------- ルート1: 解説ページ ----------------
    st.title("解説")
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
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("戻る", on_click=lambda: go_to("video1"))
    with col2:
        st.button("次へ", on_click=lambda: go_to("chat1"))

def render_chat():
    st.title("Discussion")
    api_key = st.secrets["API_KEY"]
    client = openai.OpenAI(api_key=api_key)

    if "messages" not in st.session_state:
        if st.session_state.role == 'teacher':
            role_prompt = "The conversation is intelligent and easy to understand. The goal is to help the user improve their English skills and deepen their understanding of the video's content."
        else:
            role_prompt = "The conversation is casual. Shares personal feelings and experiences."

        script_file = "script/scr-dream.txt"
        conv_file = "sample-conversation/conv-dream.txt"

        with open(script_file, "r", encoding="utf-8") as f:
            script = f.read()
        with open(conv_file, "r", encoding="utf-8") as f:
            conversation_example = f.read()

        system_prompt = f'''
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
        st.session_state.messages = [
            {"role": "system", "content": system_prompt},
            {"role": "assistant", "content": "What did you think of the video?"}
        ]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

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
        
        if st.session_state.username and st.session_state.date:
            filename = f"{st.session_state.username}_{st.session_state.date}.txt"
            with open(filename, "a", encoding="utf-8") as f:
                f.write(f"User: {prompt}\n")
                f.write(f"GPT: {reply}\n\n")

    col1, col2 = st.columns(2)
    with col1:
        st.button("戻る", on_click=lambda: go_to_and_clear_chat("explanation1"))
    with col2:
        st.button("次へ", on_click=lambda: go_to_and_clear_chat("survey"))

def render_survey():
    st.title("アンケート")
    st.write("以下のリンクからアンケートにお答えください。")
    st.markdown("[Googleフォームはこちら](https://docs.google.com/forms/d/xxxxxx)")

    if "messages" in st.session_state:
        log_text = ""
        for m in st.session_state.messages:
            if m["role"] == "user":
                log_text += f"User: {m['content']}\n"
            elif m["role"] == "assistant":
                log_text += f"GPT: {m['content']}\n"

        st.download_button(
            label="💾 会話ログをダウンロード",
            data=log_text,
            file_name=f"{st.session_state.username}_{st.session_state.date}.txt",
            mime="text/plain"
        )
        if st.button("🚀 ログを送信（GitHubに保存）"):
            # This part requires the push_to_github function, which we should move to utils
            st.warning("GitHubへの送信機能は現在リファクタリング中です。")

    col1, col2 = st.columns(2)
    with col1:
        st.button("戻る", on_click=lambda: go_to("chat1"))
    
    st.button("ホームに戻る", on_click=lambda: go_to("home"))
