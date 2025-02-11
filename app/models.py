from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.db import Base


class PromptTemplate(Base):
    __tablename__ = "prompt_templates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)  # 프롬프트 제목
    system_message = Column(Text, nullable=False)  # 시스템 메시지 (역할 정의)
    prompt_format = Column(Text, nullable=False)  # 프롬프트 포맷 (.format 사용)
    created_at = Column(DateTime, default=func.now())  # 생성 날짜
    use_yn = Column(String(1), default="y")  # 사용 여부 (y/n)


class LLMResult(Base):
    __tablename__ = "llm_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    prompt_id = Column(Integer, nullable=False)
    model_name = Column(String(50), nullable=False)  # 사용한 LLM 모델명
    api_provider = Column(String(50), nullable=False)  # LLM API 환경명 (OpenAI, Azure 등)
    response_text = Column(Text, nullable=False)  # LLM 결과 값
    token_usage = Column(Text, nullable=False)  # 사용된 토큰 정보 (JSON 형태로 저장)
    executed_at = Column(DateTime, default=func.now())  # 실행 날짜
    

class LLMReview(Base):
    __tablename__ = "llm_reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    llm_result_id = Column(Integer, nullable=False)  # 실행 결과 ID (FK)
    rating = Column(Integer, nullable=False)  # 평점 (10점 만점)
    feedback = Column(Text, nullable=True)  # 피드백 텍스트
    reviewed_at = Column(DateTime, default=func.now())  # 평가 제공 날짜
 
 
class LLMResultEdit(Base):
    __tablename__ = "llm_result_edits"

    id = Column(Integer, primary_key=True, autoincrement=True)
    llm_result_id = Column(Integer, nullable=False)  # 실행 결과 ID (FK)
    edited_text = Column(Text, nullable=False)  # 수정된 LLM 결과
    edited_at = Column(DateTime, default=func.now())  # 수정 날짜
