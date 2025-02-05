from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.schemas import PromptCreate, PromptResponse
from app.crud import create_prompt, get_prompts, get_prompt_by_id, update_prompt, delete_prompt

router = APIRouter(
    prefix="/prompts",
    tags=["prompts"]
)

# 프롬프트 생성 API
@router.post("/", response_model=PromptResponse)
def create_prompt_api(prompt: PromptCreate, db: Session = Depends(get_db)):
    return create_prompt(db, prompt)

# 전체 프롬프트 조회 API
@router.get("/", response_model=List[PromptResponse])
def get_prompts_api(db: Session = Depends(get_db)):
    return get_prompts(db)

# 특정 프롬프트 조회 API
@router.get("/{prompt_id}", response_model=PromptResponse)
def get_prompt_api(prompt_id: int, db: Session = Depends(get_db)):
    prompt = get_prompt_by_id(db, prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt

# 프롬프트 업데이트 API
@router.put("/{prompt_id}", response_model=PromptResponse)
def update_prompt_api(prompt_id: int, prompt: PromptCreate, db: Session = Depends(get_db)):
    updated_prompt = update_prompt(db, prompt_id, prompt.title, prompt.prompt_format)
    if not updated_prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return updated_prompt

# 프롬프트 삭제 (Soft Delete) API
@router.delete("/{prompt_id}")
def delete_prompt_api(prompt_id: int, db: Session = Depends(get_db)):
    deleted_prompt = delete_prompt(db, prompt_id)
    if not deleted_prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return {"message": "Prompt deleted successfully"}
