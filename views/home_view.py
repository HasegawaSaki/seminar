import streamlit as st
from utils import set_role, go_to

def render():

#名前の入力
    st.subheader("2. お名前を入力してください")
    st.session_state.username = st.text_input("お名前", label_visibility="collapsed")

# 学習の目的を選択
    st.subheader("1. 学習の目的を選択してください")
    
    teacher_btn_type = "primary" if st.session_state.role == 'teacher' else "secondary"
    classmate_btn_type = "primary" if st.session_state.role == 'classmate' else "secondary"

    col1, col2 = st.columns(2)
    with col1:
        st.button("サポート（先生）", on_click=set_role, args=('teacher',), use_container_width=True, type=teacher_btn_type)
    with col2:
        st.button("実践的な英語学習（クラスメイト）", on_click=set_role, args=('classmate',), use_container_width=True, type=classmate_btn_type)

    # レベルを選択して開始
    st.subheader("3. レベルを選択して開始")
    
    def go_to_with_check(target_page, route):
        if not st.session_state.role:
            st.warning("⚠️ 1. 学習の目的を選択してください")
        elif not st.session_state.username.strip():
            st.warning("⚠️ 2. 名前を入力してください")
        else:
            go_to(target_page, route)

    col3, col4 = st.columns(2)
    with col3:
        st.button("B2レベル", on_click=go_to_with_check, args=("video1", 1), use_container_width=True)
    with col4:
        st.button("C1レベル", on_click=go_to_with_check, args=("video2", 2), use_container_width=True)

