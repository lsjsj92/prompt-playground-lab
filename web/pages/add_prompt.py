# web/add_prompt.py
import streamlit as st
import requests
from config import API_BASE_URL

st.title("프롬프트 추가하기")

with st.form("add_prompt_form"):
    title = st.text_input("프롬프트 제목")
    system_message = st.text_area("시스템 메시지 (AI의 역할)", height=150)
    prompt_format = st.text_area("프롬프트 포맷 (변수 포함)", height=200)
    
    submitted = st.form_submit_button("프롬프트 저장")

if submitted:
    if not title or not system_message or not prompt_format:
        st.warning("모든 필드를 입력해야 합니다.")
    else:
        data = {
            "title": title,
            "system_message": system_message,
            "prompt_format": prompt_format
        }
        response = requests.post(f"{API_BASE_URL}/prompts/", json=data)
        
        if response.status_code == 200:
            st.success("프롬프트가 성공적으로 저장되었습니다!")
        else:
            st.error(f"저장 실패: {response.json()}")

