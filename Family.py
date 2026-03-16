import streamlit as st
import datetime
import json
import os
import random

# --- 1. 앱 설정 ---
st.set_page_config(page_title="우리 가족 아지트", page_icon="🏠")

DB_FILE = "family_db.json"

# --- 2. 데이터 관리 ---
def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"plans": {}, "moods": {}}

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- 3. 기념일 데이터 ---
ANNIVERSARIES = {
    "11-12": "🎂 지민(나) 생일",
    "03-03": "🎂 유정이 누나 생일",
    "12-13": "🎂 엄마 생일",
    "08-31": "🎂 아빠 생일",
    "02-03": "💍 엄마&아빠 결혼 기념일"
}

# --- 4. 메인 화면 ---
st.title("👨‍👩‍👧‍👦 우리 가족 전용 아지트")

# 로그인 (이름 선택)
user_list = ["지민", "유정이 누나", "유선이 누나", "엄마", "아빠"]
current_user = st.selectbox("👤 누구로 접속하시겠습니까?", user_list)

# [기념일 알림]
today = datetime.datetime.now().strftime("%m-%d")
if today in ANNIVERSARIES:
    st.balloons()
    st.success(f"🎊 오늘은 {ANNIVERSARIES[today]}입니다! 모두 축하해주세요! 🎊")

# [가족 소집]
if st.button("📢 가족 소집 (모두에게 알림!)"):
    st.snow()
    st.audio("https://www.soundjay.com/buttons/beep-01a.mp3")
    st.warning(f"🚨 {current_user}님이 가족 모두를 긴급 소집했습니다! 지금 앱을 확인하세요!")

st.divider()

# [기분 온도계]
st.subheader("🌡️ 오늘의 우리 가족 기분 지수")
data = load_data()
mood = st.slider(f"{current_user}의 오늘 기분은?", 0, 10, 5)

if st.button("기분 지수 기록"):
    data["moods"][current_user] = mood
    save_data(data)
    st.success("기분이 기록되었습니다!")

if data["moods"]:
    avg_mood = sum(data["moods"].values()) / len(data["moods"])
    st.info(f"현재 가족 평균 기분 지수: {avg_mood:.1f}점")

# [계획 공유]
st.divider()
st.subheader(f"📝 {current_user}의 오늘 계획")
plan = st.text_area("오늘 무엇을 할 계획인가요?")
if st.button("계획 저장"):
    data["plans"][current_user] = plan
    save_data(data)
    st.success("계획이 공유되었습니다!")

st.write("---")
st.subheader("📋 가족들의 오늘 계획")
for u in user_list:
    st.write(f"**{u}**: {data['plans'].get(u, '아직 계획 없음')}")

# [랜덤 미션]
st.divider()
if st.button("🎲 심심해! 랜덤 미션 뽑기"):
    missions = [
        "가족 단톡방에 하트 보내기! ❤️",
        "가족 중 한 명에게 칭찬 한마디 하기!",
        "오늘 저녁 메뉴는 내가 정하기!",
        "지금 당장 '사랑해'라고 말하기!"
    ]
    st.info(f"오늘의 미션: {random.choice(missions)}")

# [기념일 정보]
with st.expander("📅 우리 가족 기념일 보기"):
    for d, event in ANNIVERSARIES.items():
        st.write(f"• **{d}**: {event}")
