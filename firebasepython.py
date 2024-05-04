import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os

# 환경 변수에서 파이어베이스 인증 정보 가져오기
firebase_credential_json = os.getenv("FIREBASE_CREDENTIAL_JSON")

# 파이어베이스 서비스 계정 키 초기화
cred = credentials.Certificate(firebase_credential_json)

# 파이어베이스 앱 초기화
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://test-486a8-default-rtdb.firebaseio.com/'
})

# 데이터베이스 경로 설정
data_ref = db.reference('realPower')

# Streamlit 애플리케이션 시작
st.title('Real Power 데이터 시각화')

# 데이터 가져오기
data = data_ref.get()

# 데이터 출력
if data:
    st.write(data)
else:
    st.write('데이터를 가져올 수 없습니다.')
