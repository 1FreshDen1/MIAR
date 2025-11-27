from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional


class ReviewCreate(BaseModel):
    user_id: str
    product_id: str
    rating: float
    comment: Optional[str] = None


class ReviewResponse(BaseModel):
    id: str
    user_id: str
    product_id: str
    rating: float
    comment: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
