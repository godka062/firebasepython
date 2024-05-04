import firebase_admin
from firebase_admin import credentials, db
import streamlit as st

# Firebase 프로젝트 키 및 데이터베이스 URL 설정
cred = credentials.Certificate("C:/test/test-486a8-firebase-adminsdk-6jl9k-2bf67a04df.json")
try:
    app = firebase_admin.get_app()
except ValueError:
    app = firebase_admin.initialize_app(cred, {'databaseURL': 'https://test-486a8-default-rtdb.firebaseio.com/'})

# 파이어베이스에서 데이터 가져오기
ref = db.reference('realPower')
data = ref.get()

# 스트림릿으로 데이터 표시
st.write(data)
