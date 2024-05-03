import streamlit as st
from datetime import datetime, timedelta
from statistics import stdev

# Firebase 연동
import firebase_admin
from firebase_admin import credentials, db

# Firebase 인증 정보 로드
cred = credentials.Certificate("C:/test/test-486a8-firebase-adminsdk-6jl9k-2bf67a04df.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://test-486a8-default-rtdb.firebaseio.com/'})

# Firebase에서 데이터 가져오는 함수
def fetch_data():
    ref = db.reference('realPower')
    data = ref.get()
    if data:
        return [(datetime.strptime(key, "%Y-%m-%d %H:%M:%S"), value) for key, value in data.items()]
    else:
        return []

# 실시간 전력 모니터링
st.title("실시간 전력 모니터링")

# 데이터 업데이트 간격 설정
update_interval = st.slider("데이터 업데이트 간격 (초)", min_value=1, max_value=60, value=10, key='interval_slider')
st.write(f"데이터는 매 {update_interval} 초마다 업데이트됩니다.")

# 데이터 가져오기
data = fetch_data()

# 최근 데이터 가져오기
def get_recent_data(data):
    if len(data) > 20:
        return data[-20:]
    else:
        return data

# 최근 데이터 표시
recent_data = get_recent_data(data)
st.subheader("최근 데이터")
if data:
    for timestamp, value in recent_data:
        st.write(f"시간: {timestamp}, 전력량: {value} [W]")

# 통계 정보
st.subheader("통계 정보")
if data:
    values = [item[1] for item in data]
    st.write(f"평균: {sum(values) / len(values)} [W]")
    st.write(f"최솟값: {min(values)} [W]")
    st.write(f"최댓값: {max(values)} [W]")
    st.write(f"표준편차: {stdev(values)}")
