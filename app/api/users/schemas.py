from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """사용자 생성 스키마."""

    email: EmailStr
    password: str = Field(min_length=8)
    name: str = Field(min_length=1)


class UserUpdate(BaseModel):
    """사용자 수정 스키마."""

    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, min_length=8)
    name: Optional[str] = Field(default=None, min_length=1)


class UserResponse(BaseModel):
    """사용자 응답 스키마."""

    id: int
    email: str
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
