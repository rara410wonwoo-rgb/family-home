import streamlit as st
import datetime
import json
import os

# --- 1. 앱 설정 및 보안 설정 (에러 방지용) ---
st.set_page_config(page_title="우리 가족 아지트", page_icon="🏠")

# --- 2. 데이터 저장 로직 (가상환경 내 경로 문제 방지) ---
# 파일 이름을 절대 경로가 아닌 상대 경로로 설정하여 어디서든 실행되게 합니다.
DB_FILE = "family_notes_db.json"

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"나": [], "누나": [], "엄마": [], "아빠": []}
    return {"나": [], "누나": [], "엄마": [], "아빠": []}

def save_data(user, text):
    data = load_data()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    data[user].append({"time": now, "content": text})
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- 3. 기념일 데이터 ---
ANNIVERSARIES = {
    "11-12": "🎂 내 생일 (축하해! 🎉)",
    "03-03": "🎂 쌍둥이 누나 생일",
    "12-13": "🎂 엄마 생일",
    "08-31": "🎂 아빠 생일",
    "02-03": "💍 엄마&아빠 결혼 기념일"
}

# --- 4. 메인 화면 UI ---
st.title("👨‍👩‍👧‍👦 우리 가족 전용 공간")

# [장난 기능] 가족 소집 버튼
if st.button("📢 가족 소집 (클릭!)"):
    st.snow()  # 화면에 눈 내리는 효과
    # 실제 소리가 나는 오디오 (무료 소스)
    st.audio("https://www.soundjay.com/buttons/beep-01a.mp3")
    st.warning("🚨 누군가 가족들을 긴급하게 찾고 있어요!!!")

# 생일/기념일 체크
today = datetime.datetime.now().strftime("%m-%d")
if today in ANNIVERSARIES:
    st.balloons() # 풍선 효과
    st.success(f"🎊 오늘은 {ANNIVERSARIES[today]}입니다! 모두 한마디씩 남겨주세요! 🎊")

st.divider()

# --- 5. 가족별 전용 공간 ---
user_list = ["나", "누나", "엄마", "아빠"]
selected_user = st.sidebar.selectbox("👤 누구의 공간으로 들어갈까요?", user_list)

st.subheader(f"📍 {selected_user}의 메모장")

# 입력 폼
with st.form("note_form", clear_on_submit=True):
    user_input = st.text_area("가족에게 남길 메시지를 적어보세요.")
    submit_button = st.form_submit_button("영구 저장하기")
    
    if submit_button and user_input:
        save_data(selected_user, user_input)
        st.success("메모가 저장되었습니다!")

# 저장된 메모 불러와서 표시
st.write("---")
all_notes = load_data()
current_notes = all_notes.get(selected_user, [])

if current_notes:
    for n in reversed(current_notes):
        st.info(f"📅 {n['time']}\n\n{n['content']}")
else:
    st.write("아직 남겨진 메모가 없습니다.")

# 사이드바 기념일 정보
st.sidebar.divider()
st.sidebar.subheader("📅 가족 기념일")
for d, event in ANNIVERSARIES.items():
    st.sidebar.write(f"**{d}** : {event}")
