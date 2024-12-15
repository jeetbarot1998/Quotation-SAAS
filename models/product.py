import uuid

from sqlalchemy import Column, String, Numeric, DateTime
from sqlalchemy.orm import relationship

from models.base import TenantAwareModel, Base
from datetime import datetime


class Product(Base, TenantAwareModel):
    """
    Product model - tenant-aware
    Each product belongs to a specific organization
    """
    __tablename__ = "products"

    __tablename__ = "products"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    sku = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Add this relationship
    quotation_items = relationship("QuotationItem", back_populates="product")
