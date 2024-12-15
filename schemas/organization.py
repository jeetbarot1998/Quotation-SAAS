from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

class OrganizationBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, example="Acme Corp")
    subdomain: str = Field(..., min_length=2, max_length=50, example="acme")
    email: EmailStr = Field(..., example="admin@acmecorp.com")
    description: Optional[str] = Field(None, max_length=500, example="Leading provider of innovative solutions")

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    description: Optional[str] = Field(None, max_length=500)

class OrganizationResponse(OrganizationBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True