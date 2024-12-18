from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str
    full_name: str
    org_id: int
    created_at: datetime
    updated_at: datetime

class TokenData(BaseModel):
    user_id: int
    org_id: int
    email: Optional[str] = None
    role: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

