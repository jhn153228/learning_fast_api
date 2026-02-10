import logging

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import Session

from app.api.users.models import User
from app.api.users.schemas import UserCreate, UserResponse, UserUpdate
from app.api.users.service import UserService
from app.core.database import get_session
from app.core.security import get_current_user

router = APIRouter(prefix="/users", tags=["users"])
logger = logging.getLogger(__name__)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    request: Request,
    session: Session = Depends(get_session),
):
    """새 사용자를 생성합니다 (관리자용)."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.info(f"사용자 생성 요청 - Email: {user.email}, RequestID: {request_id}")
    try:
        created_user = UserService.create_user(session, user)
        logger.info(f"사용자 생성 완료 - ID: {created_user.id}, Email: {created_user.email}")
        return created_user
    except Exception as e:
        logger.error(f"사용자 생성 실패 - Email: {user.email}, Error: {str(e)}")
        raise


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    request: Request,
    session: Session = Depends(get_session),
):
    """특정 사용자를 조회합니다."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.info(f"사용자 조회 요청 - UserID: {user_id}, RequestID: {request_id}")
    user = UserService.get_user_by_id(session, user_id)
    if not user:
        logger.warning(f"사용자를 찾을 수 없음 - UserID: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다"
        )
    logger.info(f"사용자 조회 완료 - UserID: {user_id}, Email: {user.email}")
    return user


@router.get("", response_model=list[UserResponse])
async def list_users(
    request: Request,
    session: Session = Depends(get_session),
):
    """모든 사용자를 조회합니다."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.info(f"사용자 목록 조회 요청 - RequestID: {request_id}")
    users = UserService.get_all_users(session)
    logger.info(f"사용자 목록 조회 완료 - 총 {len(users)}명")
    return users


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    request: Request,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """사용자 정보를 수정합니다 (본인만 가능)."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.info(
        f"사용자 정보 수정 요청 - UserID: {user_id}, "
        f"CurrentUser: {current_user.id}, RequestID: {request_id}"
    )
    try:
        updated_user = UserService.update_user(session, user_id, user_update, current_user)
        logger.info(f"사용자 정보 수정 완료 - UserID: {user_id}")
        return updated_user
    except Exception as e:
        logger.error(f"사용자 정보 수정 실패 - UserID: {user_id}, Error: {str(e)}")
        raise


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    request: Request,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """사용자를 삭제합니다 (본인만 가능)."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.info(
        f"사용자 삭제 요청 - UserID: {user_id}, "
        f"CurrentUser: {current_user.id}, RequestID: {request_id}"
    )
    try:
        UserService.delete_user(session, user_id, current_user)
        logger.info(f"사용자 삭제 완료 - UserID: {user_id}")
    except Exception as e:
        logger.error(f"사용자 삭제 실패 - UserID: {user_id}, Error: {str(e)}")
        raise
