from datetime import datetime
from pydantic import BaseModel, Field

class StudyItemBase(BaseModel):
    subject: str
    topic: str
    question: str
    answer: str
    difficulty: int = Field(ge=1, le=3)

class StudyItemCreate(StudyItemBase):
    pass

class StudyItemUpdate(StudyItemBase):
    pass
class StudyItemResponse(StudyItemBase):
    item_id: int
    created_at: datetime | None = None
    
    class Config: 
        from_attributes = True
class ReviewCreate(BaseModel):
    item_id: int
    user_answer: str
    confidence: int = Field(ge=1, le=5)
    response_time: float = Field(ge=0)
class ReviewResponse(ReviewCreate):
    review_id: int
    item_id: int
    user_answer: str
    correct: bool
    confidence: int
    response_time: float
    timestamp: datetime | None = None
    expected_answer: str

    class Config:
        from_attributes = True
        
class RecommendationResponse(BaseModel):
    item_id: int
    subject: str
    topic: str
    question: str
    answer: str
    difficulty: int
    recall_probability: float
