from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserLogin(BaseModel):
    """사용자 로그인 스키마."""

    email: EmailStr
    password: str = Field(min_length=8)


class Token(BaseModel):
    """토큰 응답 스키마."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """토큰 데이터 스키마."""

    email: Optional[str] = None
