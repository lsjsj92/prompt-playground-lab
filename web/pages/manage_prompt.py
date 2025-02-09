import streamlit as st
import requests
from config import API_BASE_URL

st.title("만들어둔 프롬프트 템플릿 관리")

response = requests.get(f"{API_BASE_URL}/prompts/")
if response.status_code == 200:
    prompts = response.json()
else:
    st.error("프롬프트 목록을 가져오는 데 실패했습니다.")
    prompts = []

prompt_options = {p["title"]: p for p in prompts}
selected_title = st.selectbox("수정할 프롬프트 선택", list(prompt_options.keys()))

if selected_title:
    prompt = prompt_options[selected_title]

    with st.form("edit_prompt_form"):
        title = st.text_input("프롬프트 제목", value=prompt["title"])
        system_message = st.text_area("시스템 메시지", value=prompt["system_message"], height=200)
        prompt_format = st.text_area("프롬프트 포맷", value=prompt["prompt_format"], height=600)

        updated = st.form_submit_button("프롬프트 수정")

    if updated:
        data = {
            "title": title,
            "system_message": system_message,
            "prompt_format": prompt_format
        }
        update_response = requests.put(f"{API_BASE_URL}/prompts/{prompt['id']}", json=data)

        if update_response.status_code == 200:
            st.success("프롬프트가 성공적으로 수정되었습니다!")
        else:
            st.error(f"수정 실패: {update_response.json()}")

    if st.button("프롬프트 삭제"):
        delete_response = requests.delete(f"{API_BASE_URL}/prompts/{prompt['id']}")
        if delete_response.status_code == 200:
            st.success("프롬프트가 삭제 처리되었습니다! (use_yn = 'n')")
        else:
            st.error(f"삭제 실패: {delete_response.json()}")

