from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.crud import get_prompt_by_id, save_llm_result, get_all_llm_results, save_edited_result, get_edits_by_result_id
from app.schemas import LLMRequest, LLMResponse, LLMResultResponse, LLMResultEditCreate, LLMResultEditResponse
from app.models import LLMResult
from app.core.llm_service import call_llm_api

router = APIRouter(
    prefix="/llm",
    tags=["llm"]
)

@router.post("/execute", response_model=LLMResponse)
def execute_llm(request: LLMRequest, db: Session = Depends(get_db)):
    prompt_template = get_prompt_by_id(db, request.prompt_id)
    if not prompt_template:
        raise HTTPException(status_code=404, detail="Prompt template not found")

    # system_message에서 역할(role) 변수만 적용
    try:
        system_message = prompt_template.system_message.format(role=request.role if request.role else "AI 어시스턴트")
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing variable in system message: {str(e)}")

    # 프롬프트 본문에 사용자 입력 변수 적용
    try:
        formatted_prompt = prompt_template.prompt_format.format(**request.variables)
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing variable in prompt format: {str(e)}")

    # LLM 호출
    response = call_llm_api(request.api_provider, request.model_name, system_message, formatted_prompt)
        
    saved_result = save_llm_result(
        db=db,
        prompt_id=prompt_template.id,
        model_name=request.model_name,
        api_provider=request.api_provider,
        response_text=response["llm_result"],
        token_usage=str(response["llm_token_info"])
    )

    return {
        "id": saved_result.id,
        "llm_result": response["llm_result"],
        "llm_token_info": response["llm_token_info"]
    }

# 실행 이력 조회 API
@router.get("/results", response_model=List[LLMResultResponse])
def get_llm_results_api(db: Session = Depends(get_db)):
    return get_all_llm_results(db)

# LLM 실행 결과 수정 API
@router.put("/results/edit", response_model=LLMResultEditResponse)
def edit_llm_result(edit_data: LLMResultEditCreate, db: Session = Depends(get_db)):
    return save_edited_result(db, edit_data.llm_result_id, edit_data.edited_text)

# 특정 실행 결과의 수정 내역 조회 API
@router.get("/results/edits/{llm_result_id}", response_model=List[LLMResultEditResponse])
def get_edited_results(llm_result_id: int, db: Session = Depends(get_db)):
    return get_edits_by_result_id(db, llm_result_id)
