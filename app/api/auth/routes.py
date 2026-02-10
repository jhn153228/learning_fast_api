from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.api.auth.schemas import Token, UserLogin
from app.api.auth.service import AuthService
from app.api.users.models import User
from app.api.users.schemas import UserCreate, UserResponse
from app.core.database import get_session
from app.core.security import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(user: UserCreate, session: Session = Depends(get_session)):
    """새 사용자를 등록합니다 (회원가입)."""
    return AuthService.register(session, user)


@router.post("/login", response_model=Token)
async def login(user: UserLogin, session: Session = Depends(get_session)):
    """사용자 로그인 (JWT 토큰 발급)."""
    return AuthService.login(session, user)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """현재 로그인한 사용자 정보를 조회합니다."""
    return AuthService.get_current_user_info(current_user)
