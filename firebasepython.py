import os
import firebase_admin
from firebase_admin import db
import streamlit as st

# 환경 변수에서 서비스 계정 키 경로 가져오기
service_account_key = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Firebase 앱 초기화
try:
    app = firebase_admin.get_app()
except ValueError:
    app = firebase_admin.initialize_app(options={
        'databaseURL': 'https://test-486a8-default-rtdb.firebaseio.com/',
        'credential': firebase_admin.credentials.Certificate(service_account_key)
    })

# 파이어베이스에서 데이터 가져오기
ref = db.reference('realPower')
data = ref.get()

# 스트림릿으로 데이터 표시
st.write(data)
