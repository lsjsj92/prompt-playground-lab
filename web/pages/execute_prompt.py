import streamlit as st
import time
import requests
import re
from config import API_BASE_URL, load_config

config = load_config()

st.title("LLM 실행하기")

# DB에서 저장된 프롬프트 가져오기
response = requests.get(f"{API_BASE_URL}/prompts/")
if response.status_code == 200:
    prompts = response.json()
else:
    st.error("프롬프트 목록을 가져오는 데 실패했습니다.")
    prompts = []

# 사용자가 선택할 프롬프트 목록 생성
prompt_options = {p["title"]: p for p in prompts}
selected_title = st.selectbox("실행할 프롬프트 선택", list(prompt_options.keys()))

if selected_title:
    prompt = prompt_options[selected_title]
    st.subheader("선택한 프롬프트")
    st.text(f"Title: {prompt['title']}")
    st.text(f"System Message: {prompt['system_message']}")
    st.text(f"Prompt Format: {prompt['prompt_format']}")

    # {} 안의 변수 추출
    variable_names = re.findall(r"\{(.*?)\}", prompt["prompt_format"])
    
    # 사용자 입력 폼
    with st.form("execute_prompt_form"):
        role = st.text_area("역할 (system_message)", value=prompt['system_message'], disabled=False, height=150)
        # API 제공자 및 모델 선택
        api_provider = st.selectbox("API 제공자", list(config.LLM_PROVIDERS.keys()))
        model_name = st.selectbox("모델 선택", config.LLM_PROVIDERS[api_provider])
        
        variables = {}
        for var in variable_names:
            variables[var] = st.text_area(f"{var} 값 입력", value="", height=200)

        submitted = st.form_submit_button("실행")
    # 입력 폼 제출 할 때
    if submitted:
        if not all(variables.values()):
            st.warning("모든 변수 값을 입력해야 합니다!")
        else:
            request_data = {
                "prompt_id": prompt["id"],
                "role": role,
                "variables": variables,
                "api_provider": api_provider,
                "model_name": model_name
            }
            
            # LLM 실행 API 호출
            response = requests.post(f"{API_BASE_URL}/llm/execute", json=request_data)
        
        if response.status_code == 200:
            result = response.json()
            st.session_state["llm_result_id"] = result["id"]  # 실행 결과 ID 저장
            st.session_state["original_response"] = result["llm_result"]  # 원본 결과 저장
            st.rerun()  # 새로고침하여 값 유지

# 실행된 LLM 결과가 있을 경우 표시
if "llm_result_id" in st.session_state:
    llm_result_id = st.session_state["llm_result_id"]
    original_response = st.session_state.get("original_response", "")

    st.subheader("LLM 응답 결과")
    st.write(original_response)

    # 수정 폼
    with st.form("edit_result_form"):
        edited_response = st.text_area("LLM 결과 수정", value=original_response, height=200, key="edited_text")
        save_edit = st.form_submit_button("수정된 결과 저장")

    # 수정 버튼 클릭 시 API 호출
    if save_edit:
        edit_data = {
            "llm_result_id": llm_result_id,
            "edited_text": st.session_state["edited_text"]  # session_state에서 값 가져옴
        }
        try:
            edit_response = requests.put(f"{API_BASE_URL}/llm/results/edit", json=edit_data)
            if edit_response.status_code == 200:
                st.success("수정된 결과가 성공적으로 저장되었습니다!")
                time.sleep(2)
                st.rerun()  # 새로고침하여 최신 데이터 반영
            else:
                st.error(f"수정 저장 실패: {edit_response.json()}")
        except Exception as e:
            st.error(f"API 요청 중 오류 발생: {e}")

    # 기존 수정 내역 조회
    edits_response = requests.get(f"{API_BASE_URL}/llm/results/edits/{llm_result_id}")
    if edits_response.status_code == 200:
        edits = edits_response.json()
    else:
        edits = []

    # 기존 수정 내역을 테이블 형태로 출력
    if edits:
        st.subheader("기존 수정 내역")
        for edit in edits:
            st.write(f"**수정 날짜:** {edit['edited_at']}")
            st.write(f"**수정된 텍스트:** {edit['edited_text']}")
            st.markdown("---")
