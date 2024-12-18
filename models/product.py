import uuid

from sqlalchemy import Column, String, Numeric, DateTime, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from models.base import TenantAwareModel, Base
from datetime import datetime


class Product(Base, TenantAwareModel):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    sku = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    image_url = Column(Text, nullable=True)  # Using Text instead of String(255)
    quotation_items = relationship("QuotationItem", back_populates="product")
