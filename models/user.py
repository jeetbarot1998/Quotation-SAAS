from sqlalchemy import Column, String, DateTime, Integer
from datetime import datetime
from models import Base
from models.base import TenantAwareModel


class User(Base, TenantAwareModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    role = Column(String(50), nullable=False)  # admin, user, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
