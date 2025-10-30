import streamlit as st
from common import display_header, go_to

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
