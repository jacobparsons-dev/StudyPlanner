from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import StudyItem
from ..schemas import StudyItemResponse, StudyItemCreate, StudyItemUpdate

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
@router.delete("/{item_id}")
def delete_study_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(StudyItem).filter(StudyItem.item_id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Study item not found")
    db.delete(item)
    db.commit()
    return {"message": "Study item deleted successfully"}
@router.put("/{item_id}", response_model=StudyItemResponse)
def update_study_item(
    item_id: int,
    updated_item: StudyItemUpdate,
    db: Session = Depends(get_db)
):
    db_item = db.query(StudyItem).filter(StudyItem.item_id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Study item not found")
    db_item.subject = updated_item.subject
    db_item.topic = updated_item.topic
    db_item.question = updated_item.question
    db_item.answer = updated_item.answer
    db_item.difficulty = updated_item.difficulty

    db.commit
    db.refresh(db_item)
    return db_item
