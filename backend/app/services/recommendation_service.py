from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models import StudyItem, Review
from .memory_model import compute_recall_prob


def get_item_stats(db: Session, item_id: int):
    result = db.query(
        func.count(Review.review_id),
        func.coalesce(func.sum(Review.correct), 0),
        func.coalesce(func.avg(Review.confidence), 0),
        func.max(Review.timestamp),
    ).filter(Review.item_id == item_id).one()

    total_reviews, successful_reviews, avg_confidence, last_review_time = result

    if last_review_time is None:
        days_since_last_review = 999.0
    else:
        if isinstance(last_review_time, str):
            last_review_time = datetime.fromisoformat(last_review_time)

        if last_review_time.tzinfo is None:
            last_review_time = last_review_time.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        delta = now - last_review_time
        days_since_last_review = delta.total_seconds() / (60 * 60 * 24)

    return {
        "total_reviews": int(total_reviews),
        "successful_reviews": int(successful_reviews),
        "avg_confidence": float(avg_confidence),
        "days_since_last_review": float(days_since_last_review),
    }


def build_recommendations(db: Session, limit: int = 5):
    items = db.query(StudyItem).all()
    ranked = []

    for item in items:
        stats = get_item_stats(db, item.item_id)

        recall_probability = compute_recall_prob(
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
            "recall_probability": recall_probability,
        })

    ranked.sort(key=lambda x: x["recall_probability"])
    return ranked[:limit]