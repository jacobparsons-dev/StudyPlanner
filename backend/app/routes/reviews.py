from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Review
from ..schemas import ReviewCreate, ReviewResponse

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/", response_model=ReviewResponse)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    db_review = Review(
        item_id=review.item_id,
        correct=review.correct,
        confidence=review.confidence,
        response_time=review.response_time,
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review