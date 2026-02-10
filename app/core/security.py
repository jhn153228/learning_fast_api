from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session, select

from app.api.users.models import User
from app.core.config import settings
from app.core.database import get_session

# HTTP Bearer 스킴
security = HTTPBearer()

# Passlib CryptContext 설정 (bcrypt 사용)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenData:
    """토큰에 포함될 데이터."""

    def __init__(self, email: Optional[str] = None):
        self.email = email


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """평문 패스워드와 해시된 패스워드 비교."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """패스워드를 해시합니다."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """JWT 액세스 토큰을 생성합니다."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session),
) -> User:
    """Bearer 토큰으로부터 현재 사용자를 가져옵니다."""
    token = credentials.credentials
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="유효하지 않은 인증 정보입니다",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credential_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credential_exception

    user = session.exec(select(User).where(User.email == token_data.email)).first()

    if user is None:
        raise credential_exception

    return user
