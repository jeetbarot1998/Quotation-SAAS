from sqlalchemy import Column, String, Numeric, ForeignKey, Integer
from sqlalchemy.orm import relationship
from models.base import TenantAwareModel, Base


class QuotationItem(Base, TenantAwareModel):
    __tablename__ = "quotation_items"

    id = Column(String(36), primary_key=True)
    quotation_id = Column(String(36), ForeignKey("quotations.id"), nullable=False)
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)

    # Define relationships
    quotation = relationship("Quotation", back_populates="items")
    product = relationship("Product", back_populates="quotation_items")

class Quotation(Base, TenantAwareModel):
    """
    Quotation model - tenant-aware
    Each quotation belongs to a specific organization
    """
    __tablename__ = "quotations"

    id = Column(String(36), primary_key=True)
    quote_number = Column(String(20), nullable=False)
    customer_id = Column(String(36), ForeignKey("customers.id"))
    total_amount = Column(Numeric(10, 2), nullable=False)

    # These relationships will automatically be org-scoped
    customer = relationship("Customer")
    items = relationship("QuotationItem", back_populates="quotation")