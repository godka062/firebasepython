import streamlit as st
import firebase_admin
from firebase_admin import credentials, db, initialize_app, get_app
from datetime import datetime, timedelta
from statistics import stdev
import numpy as np

# Firebase 인증 및 초기화
cred = credentials.Certificate("C:/test/test-486a8-firebase-adminsdk-6jl9k-2bf67a04df.json")
try:
    app = get_app()
except ValueError:
    app = initialize_app(cred, {'databaseURL': 'https://test-486a8-default-rtdb.firebaseio.com/'})

ref = db.reference('realPower')

# 사용자가 선택한 업데이트 간격을 가져옴
update_interval = st.slider("데이터 업데이트 간격 (초)", min_value=1, max_value=60, value=10, key='interval_slider')
st.write(f"데이터는 매 {update_interval} 초마다 업데이트됩니다.")

def fetch_data():
    data = ref.get()
    if data:
        return [(datetime.strptime(key, "%Y-%m-%d %H:%M:%S"), value) for key, value in data.items()]
    else:
        return []

def get_recent_data(data):
    if len(data) > 20:
        return data[-20:]
    else:
        return data

def plot_graph(data, start_time, end_time):
    filtered_data = [(time, value) for time, value in data if start_time <= time <= end_time]
    x = [item[0] for item in filtered_data]
    y = [item[1] for item in filtered_data]
    min_y = min(y)
    max_y = max(y)

    fig, ax = plt.subplots(figsize=(8, 6), dpi=100)
    ax.plot(x, y, 'b-')
    
    # Add trend line
    z = np.polyfit(range(len(y)), y, 1)
    p = np.poly1d(z)
    ax.plot(x, p(range(len(y))), color='orange', linestyle='--', linewidth=2, label='Trend Line')
    
    ax.scatter(x, y, color='red')
    ax.set_xlabel('Time')
    ax.set_ylabel('Real Power [W]')
    ax.set_title('Real Power Over Time')
    ax.set_ylim(min_y - 0.1 * abs(min_y), max_y + 0.1 * abs(max_y))
    ax.set_xlim(x[0], x[-1])
    ax.legend()
    st.pyplot(fig)

st.title("실시간 전력 모니터링")

data = fetch_data()
recent_data = get_recent_data(data)
plot_graph(recent_data, recent_data[0][0], recent_data[-1][0])

st.subheader("실시간 전력")
if data:
    latest_data = data[-1]
    st.write(f"시간: {latest_data[0]}, 전력량: {latest_data[1]} [W]")

st.subheader("전체 데이터")
PAGE_SIZE = 10
num_pages = len(data) // PAGE_SIZE + 1
page_number = st.number_input("페이지 번호", min_value=1, max_value=num_pages, value=1)
start_index = (page_number - 1) * PAGE_SIZE
end_index = min(len(data), page_number * PAGE_SIZE)
with st.expander("전체 데이터 보기"):
    with st.container():
        st.write(f"페이지: {page_number} / {num_pages}, 데이터 범위: {start_index + 1} - {end_index}")
        for idx, (timestamp, value) in enumerate(data[start_index:end_index], start=start_index + 1):
            st.write(f"{idx}. 시간: {timestamp}, 전력량: {value} [W]")

st.subheader("통계 정보")
if data:
    values = [item[1] for item in data]
    st.write(f"평균: {sum(values) / len(values)} [W]")
    st.write(f"최솟값: {min(values)} [W]")
    st.write(f"최댓값: {max(values)} [W]")
    st.write(f"표준편차: {stdev(values)}")
