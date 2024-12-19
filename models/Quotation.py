from sqlalchemy import Column, String, Numeric, ForeignKey, Integer, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from models.base import TenantAwareModel, Base
from datetime import datetime


class Quotation(Base, TenantAwareModel):
    __tablename__ = "quotations"

    # Essential Fields (Never Exclude)
    id = Column(Integer, primary_key=True, autoincrement=True)
    quote_number = Column(String(50), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    validity_period = Column(DateTime, nullable=False)

    # Conditional Fields
    shipping_address = Column(Text, nullable=True)
    tax_amount = Column(Numeric(10, 2), nullable=True)
    discount_amount = Column(Numeric(10, 2), nullable=True)
    payment_terms = Column(Text, nullable=True)
    installation_required = Column(Boolean, default=False)

    # Optional Fields
    reference_number = Column(String(100), nullable=True)
    sales_rep_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    notes = Column(Text, nullable=True)

    # Industry-Specific Fields
    sla_terms = Column(Text, nullable=True)
    warranty_info = Column(Text, nullable=True)
    compliance_certificates = Column(Text, nullable=True)
    environmental_impact = Column(Text, nullable=True)
    technical_support_details = Column(Text, nullable=True)

    # Standard Tracking Fields
    status = Column(String(20), default="draft")  # draft, sent, accepted, rejected, expired
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    customer = relationship("Customer", back_populates="quotations")
    items = relationship("QuotationItem", back_populates="quotation", cascade="all, delete-orphan")
    sales_rep = relationship("User", back_populates="quotations_created")
    organization = relationship("Organization", back_populates="quotations")


class QuotationItem(Base, TenantAwareModel):
    __tablename__ = "quotation_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quotation_id = Column(Integer, ForeignKey("quotations.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    discount_percent = Column(Numeric(5, 2), default=0)
    notes = Column(Text, nullable=True)

    # Relationships
    quotation = relationship("Quotation", back_populates="items")
    product = relationship("Product", back_populates="quotation_items")
    organization = relationship("Organization", back_populates="quotation_items")

    # Standard Tracking Fields
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


