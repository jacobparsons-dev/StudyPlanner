from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import StudyItem
from ..schemas import StudyItemResponse, StudyItemCreate

router = APIRouter(prefix="/study-items", tags=["study-items"])

@router.get("/", response_model=list[StudyItemResponse])
def get_study_items(db: Session = Depends(get_db)):
    return db.query(StudyItem).all()

@router.post("/", response_model=list[StudyItemResponse])
def create_study_item(item: StudyItemCreate, db: Session = Depends(get_db)):
    db_item = StudyItem(
        subject=item.subject,
        topic=item.topic,
        question=item.question,
        answer=item.answer,
        difficulty=item.difficulty,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item