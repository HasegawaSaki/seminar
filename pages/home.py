import streamlit as st
from common import display_header

# --------セッション状態の初期化 --------
if "username" not in st.session_state:
    st.session_state.username = ""
# if "purpose" not in st.session_state:
#     st.session_state.purpose = "楽しく会話"
if "level" not in st.session_state:
    st.session_state.level = ""
if "show_warning" not in st.session_state:
   st.session_state.show_warning = False
st.session_state.purpose = "楽しく会話" #ここで固定

# -------- ページコンテンツ --------
display_header()
st.title("ホーム")
st.subheader("ユーザーネーム")
st.write("指定のユーザーネームをご入力ください。")
st.session_state.username = st.text_input(" ", placeholder="例：A1014")

# st.markdown("---")

# st.subheader("学習タイプ")
# st.write("学習したいディスカッションのタイプを選んでください。(指定がある場合は指定のタイプを選んでください。)")
# st.caption("英語の動画を視聴後、チャットボットと英語でディスカッションをします。")
# purpose = st.radio("", ["楽しく会話", "英語力の向上"])

st.markdown("---")



st.subheader("英語レベル")
st.write("ご自身の英語レベルに合ったレベルを選んでください。")

if st.session_state.show_warning:
    st.warning("⚠️画面上部にあるフォームにユーザーネームを入力してください。")

# レベル選択
level_choice = st.radio(
    "",
    ["準中級（CEFR A2 / TOEIC 225-545 / 英検 準2級 / IELTS 3.0）", 
     "中級（CEFR B1 / TOEIC 550-784 / 英検 2級 / IELTS 4.0-5.0 / TOEFL 42-71）", 
     "準上級（CEFR B2 / TOEIC 785-944 / 英検 準1級 / IELTS 5.5-6.5 / TOEFL 72-94）", 
     "上級（CEFR C1 / TOEIC 945- / 英検 1級 / IELTS 7.0-8.0 / TOEFL 95-120）"],
    label_visibility="collapsed"
)

# ボタンの配置
col1, col2 = st.columns([1, 1])

with col1:
    # 戻るボタン
    if st.button("戻る", use_container_width=True):
        st.switch_page("welcom.py")
with col2:
    # 次へボタン：ユーザー名チェックあり
    if st.button("次へ", use_container_width=True, type="primary"):
        if not st.session_state.username.strip():
            st.session_state.show_warning = True
            st.rerun()
        else:
            st.session_state.show_warning = False
            # --- レベル設定 ---
            if level_choice == "準中級（CEFR A2 / TOEIC 225-545 / 英検 準2級 / IELTS 3.0）":
                st.session_state.level = "A2"
            elif level_choice == "中級（CEFR B1 / TOEIC 550-784 / 英検 2級 / IELTS 4.0-5.0 / TOEFL 42-71）":
                st.session_state.level = "B1"
            elif level_choice == "準上級（CEFR B2 / TOEIC 785-944 / 英検 準1級 / IELTS 5.5-6.5 / TOEFL 72-94）":
                st.session_state.level = "B2"
            else:
                st.session_state.level = "C1"    
            # st.session_state.purpose = purpose
            st.switch_page("pages/video.py")

