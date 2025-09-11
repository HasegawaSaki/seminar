import streamlit as st
import openai
from utils import go_to, go_to_and_clear_chat

def render_video():
    st.title("TED動画を見る")
    st.video("https://www.youtube.com/watch?v=1VA4rIkpSp8")
    col1, col2 = st.columns(2)
    with col1:
        st.button("戻る", on_click=lambda: go_to("home"))
    with col2:
        st.button("次へ", on_click=lambda: go_to("explanation2"))

def render_explanation():
    st.title("解説")
    st.write("※準備中")
    col1, col2 = st.columns(2)
    with col1:
        st.button("戻る", on_click=lambda: go_to("video2"))
    with col2:
        st.button("次へ", on_click=lambda: go_to("chat2"))

def render_chat():
    st.title("ChatGPTと会話")
    api_key = st.secrets["API_KEY"]
    client = openai.OpenAI(api_key=api_key)

    if "messages" not in st.session_state:
        if st.session_state.role == 'teacher':
            role_prompt = "The conversation is intelligent and easy to understand. The goal is to help the user improve their English skills and deepen their understanding of the video's content."
        else:
            role_prompt = "The conversation is casual. Shares personal feelings and experiences."

        script_file = "script/scr-freight.txt"
        conv_file = "sample-conversation/conv-freight.txt"

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
- Uses specialized terminology related to the video. The conversation delves deeper into the video's content.

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
        
    col1, col2 = st.columns(2)
    with col1:
        st.button("戻る", on_click=lambda: go_to_and_clear_chat("explanation2"))
    with col2:
        st.button("次へ", on_click=lambda: go_to_and_clear_chat("survey2"))

def render_survey():
    st.title("アンケート")
    st.write("以下のリンクからアンケートにお答えください。")
    st.markdown("[Googleフォームはこちら](https://docs.google.com/forms/d/xxxxxx)")

    col1, col2 = st.columns(2)
    with col1:
        st.button("戻る", on_click=lambda: go_to("chat2"))
    
    st.button("ホームに戻る", on_click=lambda: go_to("home"))
