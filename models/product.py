from sqlalchemy import Column, String, Numeric, ForeignKey
from models.base import TenantAwareModel, Base


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
