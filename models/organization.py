from sqlalchemy import Column, String, Integer, DateTime, Text
from datetime import datetime

from sqlalchemy.orm import relationship

from models.base import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    subdomain = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    description = Column(Text, nullable=True)
    email = Column(String(100), nullable=True)

    # Relationships
    users = relationship("User", back_populates="organization")
    customers = relationship("Customer", back_populates="organization")
    products = relationship("Product", back_populates="organization")
    quotations = relationship("Quotation", back_populates="organization")
    quotation_items = relationship("QuotationItem", back_populates="organization")
