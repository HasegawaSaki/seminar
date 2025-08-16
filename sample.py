import streamlit as st
import openai

# ページ番号をセッションに保持
if "page" not in st.session_state:
    st.session_state.page = 1

def next_page():
    if st.session_state.page < 4:
        st.session_state.page += 1

def prev_page():
    if st.session_state.page > 1:
        st.session_state.page -= 1

# ページ1: TED動画ページ
if st.session_state.page == 1:
    st.title("TED動画を見る")
    st.video("https://www.youtube.com/watch?v=YXn-eNPzlo8")
    col1, col2 = st.columns(2)
    with col1:
        st.button("戻る", on_click=prev_page, disabled=True)  # 最初のページは戻れない
    with col2:
        st.button("次へ", on_click=next_page)

# ページ2: 解説ページ
elif st.session_state.page == 2:
    st.title("解説")
    st.write("""Step 1: 意味のあるまとまりごとに区切って、全文翻訳

Well, we dream for at least several different reasons.
さて、私たちは少なくともいくつかの異なる理由で夢を見ています。
One key benefit is creativity.
主な利点の一つは創造性です。
Sleep, including dream sleep, is associated with an enhanced ability to solve next-day problems.
夢を見る睡眠を含む睡眠は、翌日の問題解決能力の向上と関連しています。
It's almost as though we go to sleep with the pieces of the jigsaw, but we wake up with the puzzle complete.
まるで私たちがジグソーパズルのピースを持って眠り、目覚めたときにはパズル全体が完成しているかのようです。

The second benefit of REM-sleep dreaming is emotional first aid.
REM睡眠中の夢のもう一つの利点は感情的な応急処置です。
REM sleep takes the painful sting out of difficult emotional experiences so that when we come back the next day, we feel better about those painful events.
REM睡眠はつらい感情的経験の痛みを和らげるため、翌日それらの出来事について前よりも気分が良くなるのです。
You can almost think of dreaming as a form of overnight therapy.
夢を見ることは、一晩で行われるセラピーのようなものだと考えられるでしょう。
It's not time that heals all wounds, but it's time during dream sleep that provides emotional convalescence.
すべての傷を癒すのは単なる時間ではなく、夢の中で眠っているその時間こそが感情の回復をもたらすのです。

Now, it's not just that you dream. It's also what you dream about that seems to make a difference.
さて、夢を見ること自体だけでなく、「何について夢を見るか」も違いを生んでいるようです。
Scientists have discovered that after learning a virtual maze, for example, those individuals who slept but critically also dreamed about the maze were the only ones who ended up being better at navigating the maze when they woke up.
例えば、仮想迷路の操作を学んだ後で、眠った人の中でも特にその迷路について夢を見た人だけが、目覚めたときにより上手に迷路を進めることができると科学者たちは発見しました。
And this same principle is true for our mental health.
そして、この同じ原則は私たちの心の健康にも当てはまります。
For example, people going through a difficult or traumatic experience such as a divorce, and who are dreaming about that event, go on to gain resolution to their depression relative to those who were dreaming but not dreaming about the events themselves.
例えば、離婚のような困難やトラウマとなる経験をしている人で、その出来事について夢を見る人は、そうでない夢を見る人と比べ、うつ状態の解消に至ることがより多いのです。

All of which means that sleep and the very act of dreaming itself appears to be an essential ingredient to so much of our waking lives.
これら全ては、睡眠および夢を見るという行為そのものが、私たちの起きている時間の生活にとって不可欠な要素であることを意味しています。
We dream, therefore we are.
私たちは夢を見る。ゆえに私たちは存在する。

Step 2: 難しそうな単語10個
英単語
意味
品詞
例文
creativity
創造性
名詞
Creativity is important for artists and engineers.
associated
関連した、関係した
形容詞
Exercise is associated with good health.
enhanced
強化された、より高められた
形容詞
The new phone has enhanced features.
jigsaw
ジグソーパズル
名詞
He bought a difficult jigsaw for his daughter.
REM-sleep
レム睡眠（夢の多い深い睡眠）
名詞
REM-sleep is important for our mental health.
sting
（感情的な）痛み、ひりひりする感覚
名詞
The sting of his words lasted for days.
therapy
治療、セラピー
名詞
Music can be a kind of therapy for stress.
convalescence
回復期間
名詞
He needed a week of convalescence after surgery.
virtual
仮想の、バーチャルの
形容詞
I enjoyed the virtual museum tour on my computer.
traumatic
トラウマになる、心的外傷の
形容詞
The earthquake was a traumatic experience for many residents.


Step 3: 重要なフレーズ5つ
英語フレーズ
意味
例文
be associated with A
Aと関連している
Heart disease is associated with unhealthy eating habits.
as though S V
まるでSがVするかのように
She talks as though she knows everything.
take the sting out of A
Aの痛み・つらさを和らげる
Laughter can take the sting out of difficult situations.
a form of A
Aの一形態
Meditation is a form of relaxation.
an essential ingredient to A
Aに不可欠な要素
Trust is an essential ingredient to a happy relationship.

""")
    col1, col2 = st.columns(2)
    with col1:
        st.button("戻る", on_click=prev_page)
    with col2:
        st.button("次へ", on_click=next_page)

# ページ3: ChatGPTとの会話ページ
elif st.session_state.page == 3:
    st.title("ChatGPTと会話")
    api_key = st.secrets["API_KEY"]
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

    col1, col2 = st.columns(2)
    with col1:
        st.button("戻る", on_click=prev_page)
    with col2:
        st.button("次へ", on_click=next_page)

# ページ4: アンケートページ
elif st.session_state.page == 4:
    st.title("アンケート")
    st.write("以下のリンクからアンケートにお答えください。")
    st.markdown("[Googleフォームはこちら](https://docs.google.com/forms/d/xxxxxx)")

    col1, col2 = st.columns(2)
    with col1:
        st.button("戻る", on_click=prev_page)
    with col2:
        st.button("次へ", on_click=next_page, disabled=True)  # 最終ページは次へ無効
