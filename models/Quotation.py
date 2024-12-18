from sqlalchemy import Column, String, Numeric, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship
from models.base import TenantAwareModel, Base
from datetime import datetime

class QuotationItem(Base, TenantAwareModel):
    __tablename__ = "quotation_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quotation_id = Column(Integer, ForeignKey("quotations.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    quotation = relationship("Quotation", back_populates="items")
    product = relationship("Product", back_populates="quotation_items")


class Quotation(Base, TenantAwareModel):
    __tablename__ = "quotations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quote_number = Column(String(20), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    total_amount = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    customer = relationship("Customer")
    items = relationship("QuotationItem", back_populates="quotation")