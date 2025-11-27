from pydantic import BaseModel
from uuid import UUID

class ProductBase(BaseModel):
    name: str
    price: float
    category: str
    rating: float = 0

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: UUID

    class Config:
        orm_mode = True
