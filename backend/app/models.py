from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .db import Base

class StudyItem(Base):
    __tablename__ = "study_items"

    item_id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    difficulty = Column(Integer, default=3)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    reviews = relationship("Review", back_populates="study_item")
class Review(Base):
    __tablename__ = "reviews"
    review_id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("study_items.item_id"), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    correct = Column(Integer, nullable=False)
    confidence = Column(Integer, nullable=False)
    response_time = Column(Float, nullable=False)

    study_item = relationship("StudyItem", back_populates="reviews")
    