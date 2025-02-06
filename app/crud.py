from sqlalchemy.orm import Session
from app.models import PromptTemplate, LLMResult, LLMReview, LLMResultEdit
from app.schemas import PromptCreate

def create_prompt(db: Session, prompt_data: PromptCreate):
    '''
        만들어둔 프롬프트 저장
    '''
    db_prompt = PromptTemplate(
        title=prompt_data.title,
        system_message=prompt_data.system_message,
        prompt_format=prompt_data.prompt_format,
        use_yn="y"
    )
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

def get_prompts(db: Session):
    '''
        사용중인 프롬프트(use_yn=y) 목록 가져오기
    '''
    
    return db.query(PromptTemplate).filter(PromptTemplate.use_yn == "y").all()

def get_prompt_by_id(db: Session, prompt_id: int):
    '''
        사용중인 프롬프트(use_yn=y) 중 id에 해당되는 프롬프트 가져오기
    '''
    return db.query(PromptTemplate).filter(PromptTemplate.id == prompt_id, PromptTemplate.use_yn == "y").first()

def update_prompt(db: Session, prompt_id: int, title: str, prompt_format: str):
    '''
        프롬프트 업데이트
    '''
    db_prompt = db.query(PromptTemplate).filter(PromptTemplate.id == prompt_id).first()
    if db_prompt:
        db_prompt.title = title
        db_prompt.prompt_format = prompt_format
        db.commit()
        db.refresh(db_prompt)
    return db_prompt

def delete_prompt(db: Session, prompt_id: int):
    '''
        프롬프트 삭제(실제 삭제가 아닌, use_yn=n으로 셋팅
    '''
    db_prompt = db.query(PromptTemplate).filter(PromptTemplate.id == prompt_id).first()
    if db_prompt:
        db_prompt.use_yn = "n"
        db.commit()
        db.refresh(db_prompt)
    return db_prompt

def save_llm_result(
    db: Session, prompt_id: int, model_name: str, api_provider: str, response_text: str, token_usage: str
):
    '''
        llm 결과를 저장하는 함수
    '''
    db_result = LLMResult(
        prompt_id=prompt_id,
        model_name=model_name,
        api_provider=api_provider,
        response_text=response_text,
        token_usage=token_usage,
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result

def save_review(db: Session, llm_result_id: int, rating: int, feedback: str):
    '''
        LLM 리뷰 결과를 저장하는 함수
    '''
    db_review = LLMReview(
        llm_result_id=llm_result_id,
        rating=rating,
        feedback=feedback
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_reviews_by_result_id(db: Session, llm_result_id: int):
    '''
        리뷰 결과를 가져오는 함수
    '''
    return db.query(LLMReview).filter(LLMReview.llm_result_id == llm_result_id).all()

def get_all_llm_results(db: Session):
    '''
        llm 결과를 전부 가져옴
    '''
    return db.query(LLMResult).all()

def save_edited_result(db: Session, llm_result_id: int, edited_text: str):
    db_edit = LLMResultEdit(
        llm_result_id=llm_result_id,
        edited_text=edited_text
    )
    db.add(db_edit)
    db.commit()
    db.refresh(db_edit)
    return db_edit

def get_edits_by_result_id(db: Session, llm_result_id: int):
    return db.query(LLMResultEdit).filter(LLMResultEdit.llm_result_id == llm_result_id).all()
