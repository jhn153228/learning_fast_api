from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.core.config import settings
from app.core.database import create_db_and_tables

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
)


# 애플리케이션 시작 시 데이터베이스 테이블 생성
@app.on_event("startup")
def on_startup():
    """애플리케이션 시작 시 실행."""
    # 모델을 import하여 SQLModel이 인식하도록 함
    from app.api.users.models import User  # noqa

    create_db_and_tables()


# Include routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "message": "Welcome to FastAPI",
        "version": settings.VERSION,
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
