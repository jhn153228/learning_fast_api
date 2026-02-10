from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    PROJECT_NAME: str = "Learning FastAPI"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "FastAPI Learning Project"
    API_V1_STR: str = "/api/v1"

    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8001

    # CORS settings
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    # Database settings
    DATABASE_URL: str = (
        "postgresql://fastapi_user:fastapi_password@localhost:5432/fastapi_db"
    )
    DATABASE_ECHO: bool = True  # SQL 쿼리 로깅
    DATABASE_POOL_SIZE: int = 10  # 커넥션 풀 크기
    DATABASE_MAX_OVERFLOW: int = 20  # 최대 추가 연결 수

    # Redis settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 7379
    REDIS_DB: int = 0
    REDIS_URL: str = "redis://localhost:7379/0"

    # JWT settings
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
