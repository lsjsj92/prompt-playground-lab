from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Optional


# 프롬프트 저장 요청 모델
class PromptCreate(BaseModel):
    title: str
    system_message: str
    prompt_format: str

# 프롬프트 응답 모델
class PromptResponse(BaseModel):
    id: int
    title: str
    system_message: str
    prompt_format: str
    created_at: datetime
    use_yn: str

    class Config:
        orm_mode = True

class LLMRequest(BaseModel):
    prompt_id: int               # 사용할 프롬프트 ID
    role: Optional[str] = None   # 역할을 별도 필드로 분리
    variables: Dict[str, str]    # 프롬프트 본문에서 사용할 변수
    use_azure: bool = False      # Azure API 사용 여부
    api_provider: str  # OpenAI 또는 Azure OpenAI
    model_name: str    # gpt-4o 또는 gpt-4o-mini

class TokenUsage(BaseModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int

class LLMResponse(BaseModel):
    id: int
    llm_result: str
    llm_token_info: TokenUsage
    
class LLMResultResponse(BaseModel):
    id: int
    prompt_id: int
    model_name: str
    api_provider: str
    response_text: str
    token_usage: str
    executed_at: datetime

class ReviewCreate(BaseModel):
    llm_result_id: int
    rating: int
    feedback: Optional[str] = None

class ReviewResponse(BaseModel):
    id: int
    llm_result_id: int
    rating: int
    feedback: Optional[str]
    reviewed_at: datetime

class LLMResultEditCreate(BaseModel):
    llm_result_id: int
    edited_text: str

class LLMResultEditResponse(BaseModel):
    id: int
    llm_result_id: int
    edited_text: str
    edited_at: datetime