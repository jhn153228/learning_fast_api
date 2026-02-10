import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.core.config import settings
from app.core.database import create_db_and_tables
from app.core.exception_handlers import http_exception_handler
from app.core.logging_config import setup_logging
from app.core.middleware import RequestIDMiddleware, ResponseTimeMiddleware

# 로깅 설정
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
)

# 예외 핸들러 추가
app.add_exception_handler(Exception, http_exception_handler)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Process-Time"],
)

# Request ID 미들웨어 추가
app.add_middleware(RequestIDMiddleware)

# 응답 시간 측정 미들웨어 추가
app.add_middleware(ResponseTimeMiddleware)


# 애플리케이션 시작 시 데이터베이스 테이블 생성
@app.on_event("startup")
def on_startup():
    """애플리케이션 시작 시 실행."""
    logger.info("애플리케이션 시작 중...")
    # 모델을 import하여 SQLModel이 인식하도록 함
    from app.api.users.models import User  # noqa

    create_db_and_tables()
    logger.info("데이터베이스 테이블 생성 완료")
    logger.info(f"CORS 설정: {settings.BACKEND_CORS_ORIGINS}")
    logger.info("애플리케이션 시작 완료")


# Include routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")


@app.get("/")
async def root():
    logger.info("Root 엔드포인트 호출됨")
    return {
        "message": "Welcome to FastAPI",
        "version": settings.VERSION,
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    logger.info("Health check 엔드포인트 호출됨")
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
