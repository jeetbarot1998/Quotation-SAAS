from typing import Optional

from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    price: Decimal
    sku: str
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True