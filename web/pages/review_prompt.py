import time
import streamlit as st
import requests
import pandas as pd
from config import API_BASE_URL

st.title("LLM 실행 이력 조회 및 평가")

# 실행 이력 조회
response = requests.get(f"{API_BASE_URL}/llm/results")
if response.status_code == 200:
    results = response.json()

    # 각 실행 결과에 대해 수정된 텍스트가 있는지 확인
    for result in results:
        edits_response = requests.get(f"{API_BASE_URL}/llm/results/edits/{result['id']}")
        if edits_response.status_code == 200 and edits_response.json():
            # 최신 수정본 가져오기 (최신 순으로 정렬된 첫 번째 데이터)
            edited_result = edits_response.json()[0]  
            result["response_text"] = edited_result["edited_text"]  # 수정된 텍스트로 대체

else:
    st.error("실행 이력을 가져오는 데 실패했습니다.")
    results = []

# 실행 이력 목록 테이블로 출력
if results:
    df = pd.DataFrame(results)

    st.subheader("실행 이력 목록")

    st.dataframe(df)  # 게시판 형태로 출력

    # 선택할 실행 이력
    selected_result_id = st.selectbox("🔍 리뷰할 실행 결과 선택", df["id"])

    # 선택한 실행 결과 상세 정보 표시
    selected_result = next((r for r in results if r["id"] == selected_result_id), None)

    if selected_result:
        st.subheader("실행 결과 상세 정보")
        st.write(f"**LLM 모델:** {selected_result['model_name']}")
        st.write(f"**API 환경:** {selected_result['api_provider']}")
        st.write(f"**실행 날짜:** {selected_result['executed_at']}")
        st.write(f"**LLM 결과:** {selected_result['response_text']}")
        st.json(selected_result["token_usage"])

        # 기존 리뷰 조회 후 테이블로 출력
        reviews_response = requests.get(f"{API_BASE_URL}/reviews/{selected_result_id}")
        if reviews_response.status_code == 200:
            reviews = reviews_response.json()
        else:
            reviews = []

        if reviews:
            st.subheader("기존 리뷰 목록")
            review_df = pd.DataFrame(reviews)
            review_df = review_df[["rating", "feedback", "reviewed_at"]]  # 테이블로 정리
            st.dataframe(review_df)  # 기존 리뷰를 테이블로 출력

        # 새로운 리뷰 입력
        with st.form("review_form"):
            rating = st.slider("평점 (10점 만점)", min_value=1, max_value=10, value=5)
            feedback = st.text_area("피드백 (선택 사항)")
            submitted = st.form_submit_button("평가 저장")

        if submitted:
            review_data = {
                "llm_result_id": selected_result_id,
                "rating": rating,
                "feedback": feedback
            }
            review_response = requests.post(f"{API_BASE_URL}/reviews/", json=review_data)

            if review_response.status_code == 200:
                st.success("평가가 성공적으로 저장되었습니다!")
                time.sleep(1)
                st.rerun()
            else:
                st.error(f"평가 저장 실패: {review_response.json()}")


