from sqlalchemy import Column, String, ForeignKey, Integer, DateTime
from datetime import datetime
from models.base import TenantAwareModel, Base


class Customer(Base, TenantAwareModel):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
