import streamlit as st
from common import display_header, go_to

# --------セッション状態の初期化 --------
if "username" not in st.session_state:
    st.session_state.username = ""
if "purpose" not in st.session_state:
    st.session_state.purpose = "楽しく会話"
if "level" not in st.session_state:
    st.session_state.level = ""
if "show_warning" not in st.session_state:
   st.session_state.show_warning = False

# -------- ページコンテンツ --------
display_header()
st.title("ホーム")
st.subheader("ユーザーネーム")
st.write("指定のユーザーネームをご入力ください")
st.session_state.username = st.text_input(" ", placeholder="例：A1014")

st.markdown("---")

st.subheader("学習タイプ")
st.write("学習したいディスカッションのタイプを選んでください(指定がある場合は指定のタイプを選んでください。英語の動画を見ていただいた後、AIと英語でディスカッションをしていただきます)")
purpose = st.radio("", ["楽しく会話", "英語力の向上"])

def go_with_check(level):
    if not st.session_state.username.strip():
        st.session_state.show_warning = True
    else:
        st.session_state.show_warning = False
        go_to("video", level=level, purpose=purpose)

st.markdown("---")

if st.session_state.show_warning:
    st.warning("⚠️画面上部にあるフォームにユーザーネームを入力してください。")

st.subheader("英語レベル")
st.write("ご自身の英語レベルに合ったレベルを選んでください。レベルの詳細は下記をご覧ください。")
# ボタンの配置

col1, col2 = st.columns([1, 1])

with col1:
    # 初級：ユーザー名チェックあり
    if st.button("初級", use_container_width=True, type="primary"):
        if not st.session_state.username.strip():
            st.session_state.show_warning = True
            st.rerun()
        else:
            st.session_state.show_warning = False
            st.session_state.level = "B2"
            st.session_state.purpose = purpose
            st.switch_page("pages/2_video.py")
with col2:
    # 上級：ユーザー名チェックあり
    if st.button("上級", use_container_width=True, type="primary"):
        if not st.session_state.username.strip():
            st.session_state.show_warning = True
            st.rerun()
        else:
            st.session_state.show_warning = False
            st.session_state.level = "C1"
            st.session_state.purpose = purpose
            st.switch_page("pages/2_video.py")

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
st.button("戻る", on_click=lambda: go_to("home.py"))
