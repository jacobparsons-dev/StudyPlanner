from datetime import datetime
from pydantic import BaseModel

class StudyItemBase(BaseModel):
    subject: str
    topic: str
    question: str
    answer: str
    difficulty: str

class StudyItemResponse(StudyItemBase):
    item_id: int
    created_at: datetime | None = None
    
    class Config: 
        from_attributes = True
class ReviewCreate(BaseModel):
    item_id: int
    correct: int
    confidence: int
    response_time: float
class ReviewResponse(ReviewCreate):
    review_id: int
    timestamp: datetime | None = None

    class Config:
        from_attributes = True
        
class RecommendationResponse(BaseModel):
    item_id: int
    subject: str
    topic: str
    question: str
    answer: str
    difficulty: int
    recall_prob: float
