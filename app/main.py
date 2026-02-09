from fastapi import FastAPI
from app.api.routes import hello
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
)

# Include routers
app.include_router(hello.router, prefix="/api/v1", tags=["hello"])


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

