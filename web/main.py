import streamlit as st

st.set_page_config(page_title="프롬프트 관리", layout="wide")

with st.sidebar:
    st.title("메뉴를 선택해주세요.")

info_page = st.Page("pages/info.py", title="페이지 정보", icon=":material/assignment:")
add_prompt_page = st.Page("pages/add_prompt.py", title="프롬프트 추가하기", icon=":material/apps:")
manage_prompt_page = st.Page("pages/manage_prompt.py", title="만들어둔 프롬프트 관리하기", icon=":material/apps:")
execute_prompt_page = st.Page("pages/execute_prompt.py", title="프롬프트 실행하기(LLM)", icon=":material/apps:")
review_prompt_page = st.Page("pages/review_prompt.py", title="프롬프트 실행결과 평가하기", icon=":material/apps:")

pg = st.navigation([info_page, add_prompt_page, manage_prompt_page, execute_prompt_page, review_prompt_page])

pg.run()
