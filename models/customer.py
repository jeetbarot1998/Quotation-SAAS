from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base
from models.base import TenantAwareModel, Base


class Customer(Base, TenantAwareModel):
    """
    Customer model - tenant-aware
    Each customer belongs to a specific organization
    """
    __tablename__ = "customers"

    id = Column(String(36), primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)