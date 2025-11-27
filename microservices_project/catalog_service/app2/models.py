from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    rating = Column(Float, default=0.0, nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.rating is None:
            self.rating = 0.0
