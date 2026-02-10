from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.api.users.models import User
from app.api.users.schemas import UserCreate, UserResponse, UserUpdate
from app.api.users.service import UserService
from app.core.database import get_session
from app.core.security import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, session: Session = Depends(get_session)):
    """새 사용자를 생성합니다 (관리자용)."""
    return UserService.create_user(session, user)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, session: Session = Depends(get_session)):
    """특정 사용자를 조회합니다."""
    user = UserService.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다"
        )
    return user


@router.get("", response_model=list[UserResponse])
async def list_users(session: Session = Depends(get_session)):
    """모든 사용자를 조회합니다."""
    return UserService.get_all_users(session)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """사용자 정보를 수정합니다 (본인만 가능)."""
    return UserService.update_user(session, user_id, user_update, current_user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """사용자를 삭제합니다 (본인만 가능)."""
    UserService.delete_user(session, user_id, current_user)
