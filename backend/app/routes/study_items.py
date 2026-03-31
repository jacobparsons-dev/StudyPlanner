from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import StudyItem
from ..schemas import StudyItemResponse

router = APIRouter(prefix="/study-items", tags=["study-items"])

@router.get("/", response_model=list[StudyItemResponse])
def get_study_items(db: Session = Depends(get_db)):
    return db.query(StudyItem).all()