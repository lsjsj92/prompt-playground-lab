from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.crud import save_review, get_reviews_by_result_id
from app.schemas import ReviewCreate, ReviewResponse

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"]
)

@router.post("/", response_model=ReviewResponse)
def create_review_api(review: ReviewCreate, db: Session = Depends(get_db)):
    return save_review(db, review.llm_result_id, review.rating, review.feedback)

@router.get("/{llm_result_id}", response_model=List[ReviewResponse])
def get_reviews_api(llm_result_id: int, db: Session = Depends(get_db)):
    return get_reviews_by_result_id(db, llm_result_id)
