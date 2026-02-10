from datetime import datetime
from typing import Optional

from sqlalchemy import Index
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """사용자 모델."""

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(
        unique=True,
        index=True,
        max_length=255,
        description="사용자 이메일 주소",
    )
    hashed_password: str = Field(max_length=255, description="해시된 패스워드")
    name: str = Field(max_length=100, description="사용자 이름")
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="생성 시간",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="수정 시간",
    )

    __table_args__ = (
        Index("idx_user_email", "email"),
        Index("idx_user_created_at", "created_at"),
    )
