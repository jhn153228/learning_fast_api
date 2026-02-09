from fastapi import FastAPI
from app.api.routes import hello, users
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
    create_db_and_tables()

# Include routers
app.include_router(hello.router, prefix="/api/v1", tags=["hello"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])


@app.get("/")
async def root():
    return {
        "message": "Welcome to FastAPI",
        "version": settings.VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )

