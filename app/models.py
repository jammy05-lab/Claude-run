from datetime import date
from sqlalchemy import Column, Integer, String, Float, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    notes = Column(Text, nullable=False)
    category = Column(String(100), nullable=True)
    created_at = Column(Date, default=date.today)

    next_review_date = Column(Date, default=date.today)
    interval_days = Column(Integer, default=1)
    ease_factor = Column(Float, default=2.5)
    review_count = Column(Integer, default=0)

    reviews = relationship("ReviewLog", back_populates="topic")


class ReviewLog(Base):
    __tablename__ = "review_logs"

    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    reviewed_at = Column(Date, default=date.today)
    rating = Column(Integer, nullable=False)

    topic = relationship("Topic", back_populates="reviews")
