from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.api.users.models import User
from app.api.users.schemas import UserCreate, UserUpdate
from app.core.security import get_password_hash


class UserService:
    """사용자 관련 비즈니스 로직을 처리하는 서비스"""

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> User | None:
        """이메일로 사용자 조회"""
        return session.exec(select(User).where(User.email == email)).first()

    @staticmethod
    def get_user_by_id(session: Session, user_id: int) -> User | None:
        """ID로 사용자 조회"""
        return session.get(User, user_id)

    @staticmethod
    def get_all_users(session: Session) -> list[User]:
        """모든 사용자 조회"""
        return session.exec(select(User)).all()

    @staticmethod
    def create_user(session: Session, user_data: UserCreate) -> User:
        """새 사용자 생성"""
        # 이메일 중복 확인
        existing_user = UserService.get_user_by_email(session, user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이메일이 이미 등록되어 있습니다",
            )

        # 패스워드 해싱
        hashed_password = get_password_hash(user_data.password)

        # 사용자 생성
        db_user = User(
            email=user_data.email, hashed_password=hashed_password, name=user_data.name
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

    @staticmethod
    def update_user(
        session: Session, user_id: int, user_update: UserUpdate, current_user: User
    ) -> User:
        """사용자 정보 수정"""
        user = UserService.get_user_by_id(session, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="사용자를 찾을 수 없습니다",
            )

        # 권한 확인: 본인만 수정 가능
        if current_user.id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="다른 사용자의 정보를 수정할 수 없습니다",
            )

        # 업데이트 데이터 처리
        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                if field == "password":
                    # 패스워드는 해싱하여 저장
                    setattr(user, "hashed_password", get_password_hash(value))
                else:
                    setattr(user, field, value)

        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def delete_user(session: Session, user_id: int, current_user: User) -> None:
        """사용자 삭제"""
        user = UserService.get_user_by_id(session, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="사용자를 찾을 수 없습니다",
            )

        # 권한 확인: 본인만 삭제 가능
        if current_user.id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="다른 사용자를 삭제할 수 없습니다",
            )

        session.delete(user)
        session.commit()
