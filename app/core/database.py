from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings

# PostgreSQL 데이터베이스 엔진 생성
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # SQL 쿼리 로깅 (개발 환경용)
    pool_pre_ping=True,  # 연결 상태 확인
    pool_size=10,  # 커넥션 풀 크기
    max_overflow=20,  # 최대 추가 연결 수
)


def create_db_and_tables():
    """데이터베이스 및 테이블 생성."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """데이터베이스 세션 생성."""
    with Session(engine) as session:
        yield session
