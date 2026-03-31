from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..db import get_db
from ..models import StudyItem, Review
from ..schemas import RecommendationResponse

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(ROOT_DIR))

from ml.memory_model import compute_recall_prob

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


def get_item_stats(db: Session, item_id: int):
    result = db.query(
        func.count(Review.review_id),
        func.coalesce(func.sum(Review.correct), 0),
        func.coalesce(func.avg(Review.confidence), 0),
        func.max(Review.timestamp),
    ).filter(Review.item_id == item_id).one()

    total_reviews, successful_reviews, avg_confidence, last_review_time = result

    if last_review_time is None:
        days_since_last_review = 999
    else:
        now = datetime.now()
        if isinstance(last_review_time, str):
            last_review_time = datetime.fromisoformat(last_review_time)
        delta = now - last_review_time
        days_since_last_review = delta.total_seconds() / (60 * 60 * 24)

    return {
        "total_reviews": total_reviews,
        "successful_reviews": successful_reviews,
        "avg_confidence": avg_confidence,
        "days_since_last_review": days_since_last_review,
    }


@router.get("/", response_model=list[RecommendationResponse])
def get_recommendations(limit: int = 5, db: Session = Depends(get_db)):
    items = db.query(StudyItem).all()
    ranked = []

    for item in items:
        stats = get_item_stats(db, item.item_id)

        recall_prob = compute_recall_prob(
            days_since_review=stats["days_since_last_review"],
            successful_reviews=stats["successful_reviews"],
            avg_confidence=stats["avg_confidence"],
            difficulty=item.difficulty,
        )

        ranked.append({
            "item_id": item.item_id,
            "subject": item.subject,
            "topic": item.topic,
            "question": item.question,
            "answer": item.answer,
            "difficulty": item.difficulty,
            "recall_prob": recall_prob,
        })

    ranked.sort(key=lambda x: x["recall_prob"])
    return ranked[:limit]