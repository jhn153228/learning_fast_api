import logging

from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings

logger = logging.getLogger(__name__)

# PostgreSQL 데이터베이스 엔진 생성
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,  # SQL 쿼리 로깅
    pool_pre_ping=True,  # 연결 상태 확인
    pool_size=settings.DATABASE_POOL_SIZE,  # 커넥션 풀 크기
    max_overflow=settings.DATABASE_MAX_OVERFLOW,  # 최대 추가 연결 수
    pool_recycle=3600,  # 1시간마다 연결 재생성
    pool_timeout=30,  # 연결 대기 시간 (초)
)


# SQLAlchemy 이벤트 리스너 - 연결 시 로깅
@event.listens_for(Engine, "connect")
def receive_connect(dbapi_conn, connection_record):
    """데이터베이스 연결 시 로깅."""
    logger.info("데이터베이스 연결 성공")


# SQLAlchemy 이벤트 리스너 - 체크아웃 시 로깅
@event.listens_for(Engine, "checkout")
def receive_checkout(dbapi_conn, connection_record, connection_proxy):
    """연결 풀에서 연결 체크아웃 시 로깅."""
    logger.debug("데이터베이스 연결 체크아웃")


def create_db_and_tables():
    """데이터베이스 및 테이블 생성.

    주의: 프로덕션 환경에서는 Alembic 마이그레이션을 사용하세요.
    이 함수는 개발 환경에서만 사용하는 것을 권장합니다.
    """
    logger.info("데이터베이스 테이블 생성 시작")
    logger.warning(
        "SQLModel.metadata.create_all()을 사용 중입니다. "
        "프로덕션에서는 'alembic upgrade head'를 사용하세요."
    )
    SQLModel.metadata.create_all(engine)
    logger.info("데이터베이스 테이블 생성 완료")


def get_session():
    """데이터베이스 세션 생성."""
    with Session(engine) as session:
        logger.debug("데이터베이스 세션 생성")
        try:
            yield session
        finally:
            logger.debug("데이터베이스 세션 종료")
