# 빌드 단계
FROM python:3.13-slim as builder

WORKDIR /app

# uv 설치
RUN pip install --no-cache-dir uv

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 프로젝트 파일 복사
COPY pyproject.toml ./
# uv.lock이 있으면 복사 (없으면 무시)
COPY uv.lock* ./

# uv를 사용하여 의존성 설치
RUN uv pip install --system bcrypt>=4.2.0 && \
    uv pip install --system "passlib[bcrypt]>=1.7.4" && \
    uv pip install --system psycopg2-binary>=2.9.9 fastapi>=0.128.0 uvicorn>=0.40.0 pydantic-settings>=2.0.0 sqlmodel>=0.0.32 redis>=5.0.0 rq>=1.15.0 python-dotenv>=1.0.0 email-validator>=2.0.0 "python-jose[cryptography]>=3.3.0" python-multipart>=0.0.6

# 실행 단계
FROM python:3.13-slim

WORKDIR /app

# curl 설치 (헬스체크용) 및 PostgreSQL 클라이언트 라이브러리
RUN apt-get update && apt-get install -y \
    curl \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# 빌더에서 설치된 패키지 복사
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 애플리케이션 코드 복사
COPY app /app/app

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]

