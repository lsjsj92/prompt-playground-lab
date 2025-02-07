from fastapi import FastAPI
from app.db import init_db
from app.routers import prompt, llm, review  # 여러 개의 라우터 추가

app = FastAPI(
    title="Prompt Engineering API",
    description="FastAPI 기반 LLM 프롬프트 엔진 API",
    version="1.0.0"
)

# DB 초기화
init_db()

# API 라우터 등록
app.include_router(prompt.router)
app.include_router(llm.router)
app.include_router(review.router)

# 기본 라우트
@app.get("/")
def root():
    return {"message": "Prompt Engineering API is running!"}

# Health Check API
@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "ok", "message": "API is healthy"}
