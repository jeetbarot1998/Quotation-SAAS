from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

from models.base import Base


class Organization( Base):
    """
    Organization model - represents a tenant
    This is NOT tenant-aware as it's the tenant definition itself
    """
    __tablename__ = "organizations"

    id = Column(String(36), primary_key=True)
    name = Column(String(100), nullable=False)
    subdomain = Column(String(50), unique=True, nullable=False)