from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    price: Decimal

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True