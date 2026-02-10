import logging

from fastapi import APIRouter, Depends, Request, status
from sqlmodel import Session

from app.api.auth.schemas import Token, UserLogin
from app.api.auth.service import AuthService
from app.api.users.models import User
from app.api.users.schemas import UserCreate, UserResponse
from app.core.database import get_session
from app.core.security import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])
logger = logging.getLogger(__name__)


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(
    user: UserCreate,
    request: Request,
    session: Session = Depends(get_session),
):
    """새 사용자를 등록합니다 (회원가입)."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.info(f"회원가입 요청 - Email: {user.email}, RequestID: {request_id}")
    try:
        registered_user = AuthService.register(session, user)
        logger.info(f"회원가입 완료 - Email: {user.email}, UserID: {registered_user.id}")
        return registered_user
    except Exception as e:
        logger.error(f"회원가입 실패 - Email: {user.email}, Error: {str(e)}")
        raise


@router.post("/login", response_model=Token)
async def login(
    user: UserLogin,
    request: Request,
    session: Session = Depends(get_session),
):
    """사용자 로그인 (JWT 토큰 발급)."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.info(f"로그인 요청 - Email: {user.email}, RequestID: {request_id}")
    try:
        token = AuthService.login(session, user)
        logger.info(f"로그인 성공 - Email: {user.email}")
        return token
    except Exception as e:
        logger.warning(f"로그인 실패 - Email: {user.email}, Error: {str(e)}")
        raise


@router.get("/me", response_model=UserResponse)
async def get_me(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    """현재 로그인한 사용자 정보를 조회합니다."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.info(
        f"현재 사용자 정보 조회 - UserID: {current_user.id}, RequestID: {request_id}"
    )
    return AuthService.get_current_user_info(current_user)
