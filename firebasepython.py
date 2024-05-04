import firebase_admin
from firebase_admin import db
import streamlit as st

try:
    app = firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app()

# 파이어베이스에서 데이터 가져오기
ref = db.reference('realPower')
data = ref.get()

# 스트림릿으로 데이터 표시
st.write(data)
