from datetime import timedelta
from fastapi import HTTPException, status
from sqlmodel import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
)
from app.core.config import settings
from app.services.user_service import UserService


class AuthService:
    """인증 관련 비즈니스 로직을 처리하는 서비스"""

    @staticmethod
    def register(session: Session, user_data: UserCreate) -> User:
        """회원가입"""
        return UserService.create_user(session, user_data)

    @staticmethod
    def login(session: Session, login_data: UserLogin) -> dict:
        """로그인 및 JWT 토큰 발급"""
        # 이메일로 사용자 조회
        db_user = UserService.get_user_by_email(session, login_data.email)

        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이메일 또는 패스워드가 올바르지 않습니다",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # 패스워드 검증
        if not verify_password(login_data.password, db_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이메일 또는 패스워드가 올바르지 않습니다",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # JWT 토큰 생성
        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token = create_access_token(
            data={"sub": db_user.email},
            expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}

    @staticmethod
    def get_current_user_info(current_user: User) -> User:
        """현재 로그인한 사용자 정보 반환"""
        return current_user

