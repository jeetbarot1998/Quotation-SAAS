from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from models.base import TenantAwareModel


Base = declarative_base()

class Product(Base, TenantAwareModel):
    """
    Product model - tenant-aware
    Each product belongs to a specific organization
    """
    __tablename__ = "products"

    id = Column(String(36), primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    sku = Column(String(50), nullable=False)

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