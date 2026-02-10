from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.core.database import get_session
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
    UserLogin,
    Token,
)
from app.services.auth_service import AuthService
from app.services.user_service import UserService

router = APIRouter()


# ==================== 인증 엔드포인트 ====================

@router.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user: UserCreate,
    session: Session = Depends(get_session)
):
    """새 사용자를 등록합니다 (회원가입)."""
    return AuthService.register(session, user)


@router.post("/auth/login", response_model=Token)
async def login(
    user: UserLogin,
    session: Session = Depends(get_session)
):
    """사용자 로그인 (JWT 토큰 발급)."""
    return AuthService.login(session, user)


@router.get("/auth/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """현재 로그인한 사용자 정보를 조회합니다."""
    return AuthService.get_current_user_info(current_user)


# ==================== 사용자 CRUD 엔드포인트 ====================

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    session: Session = Depends(get_session)
):
    """새 사용자를 생성합니다 (관리자용)."""
    return UserService.create_user(session, user)


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    session: Session = Depends(get_session)
):
    """특정 사용자를 조회합니다."""
    user = UserService.get_user_by_id(session, user_id)
    if not user:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다"
        )
    return user


@router.get("/users", response_model=list[UserResponse])
async def list_users(session: Session = Depends(get_session)):
    """모든 사용자를 조회합니다."""
    return UserService.get_all_users(session)


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """사용자 정보를 수정합니다 (본인만 가능)."""
    return UserService.update_user(session, user_id, user_update, current_user)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """사용자를 삭제합니다 (본인만 가능)."""
    UserService.delete_user(session, user_id, current_user)

