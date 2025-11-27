from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

from .database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    product_id = Column(String, nullable=False)
    rating = Column(Float, nullable=False)
    comment = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
