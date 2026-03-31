from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..schemas import RecommendationResponse
from ..services.recommendation_service import build_recommendations

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/", response_model=list[RecommendationResponse])
def get_recommendations(limit: int = 5, db: Session = Depends(get_db)):
    return build_recommendations(db, limit)