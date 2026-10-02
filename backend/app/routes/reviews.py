from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Review, StudyItem
from ..schemas import ReviewCreate, ReviewResponse
from ..services.answer_evaluator import evaluate_answer

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/", response_model=ReviewResponse)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):

    # Find the study item
    item = (
        db.query(StudyItem)
        .filter(StudyItem.item_id == review.item_id)
        .first()
    )
    if not item:
        raise HTTPException(
            status_code=404,
            detail="Study Item not found"
        )
    is_correct = evaluate_answer(
        review.user_answer,
        item.answer
    )
    db_review = Review(
        item_id=review.item_id,
        correct=int(is_correct),
        confidence=review.confidence,
        response_time=review.response_time,
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return {
        "review_id": db_review.review_id,
        "item_id": db_review.item_id,
        "user_answer": review.user_answer,
        "correct": is_correct,
        "confidence": db_review.confidence,
        "response_time": db_review.response_time,
        "timestamp": db_review.timestamp,
        "expected_answer": item.answer,
    }