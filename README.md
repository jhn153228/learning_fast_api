# FastAPI Learning Project

이 프로젝트는 FastAPI의 대중적인 디렉토리 구조를 따릅니다.

## 프로젝트 구조

```
learning_fast_api/
├── app/                       # 메인 애플리케이션 패키지
│   ├── __init__.py
│   ├── main.py               # FastAPI 앱 인스턴스 및 라우터 설정
│   ├── api/                  # API 관련 코드
│   │   ├── __init__.py
│   │   └── routes/           # API 라우트 모듈
│   │       ├── __init__.py
│   │       ├── hello.py      # Hello 엔드포인트
│   │       └── users.py      # User CRUD 엔드포인트
│   ├── core/                 # 핵심 설정 및 유틸리티
│   │   ├── __init__.py
│   │   ├── config.py         # 설정 관리 (환경 변수)
│   │   ├── database.py       # 데이터베이스 연결 설정
│   │   └── redis_queue.py    # Redis Queue 설정
│   ├── models/               # 데이터베이스 모델
│   │   ├── __init__.py
│   │   └── user.py           # User 모델 (SQLModel)
│   ├── schemas/              # Pydantic 스키마
│   │   ├── __init__.py
│   │   ├── hello.py          # Hello 응답 스키마
│   │   └── user.py           # User 요청/응답 스키마
│   └── services/             # 비즈니스 로직
│       └── __init__.py
├── docker/                    # Docker 관련 파일
│   ├── Dockerfile            # 애플리케이션 이미지 정의
│   ├── .dockerignore         # Docker 빌드 제외 파일
│   ├── docker-compose.yml    # Docker Compose 설정
│   └── DOCKER_GUIDE.md       # Docker 사용 가이드
├── scripts/                   # 스크립트 파일
├── .env                       # 환경 변수 설정
├── .env.example               # 환경 변수 예제
├── pyproject.toml             # 프로젝트 의존성 및 설정
├── README.md                  # 이 파일
└── test_main.http             # HTTP 테스트 파일
```

## 주요 기능

### 1. PostgreSQL 데이터베이스
- SQLModel을 사용한 안전한 ORM
- User 모델: id, email, password, name, created_at, updated_at
- 프로덕션급 관계형 데이터베이스로 안정적이고 확장 가능

### 2. Redis 캐시 및 큐
- Redis를 이용한 캐싱
- RQ (Redis Queue)를 사용한 백그라운드 작업 처리

### 3. Docker & Docker Compose
- 멀티 컨테이너 애플리케이션 관리
- FastAPI, PostgreSQL, Redis 통합 관리
- RQ Worker를 통한 백그라운드 작업 처리

## 설치 및 실행

### 방법 1: Docker Compose (권장)

```bash
# docker 디렉토리로 이동
cd docker

# 모든 서비스 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f app

# 서비스 중지
docker-compose down
```

**접속 URL**: http://localhost:8001

자세한 내용은 [docker/DOCKER_GUIDE.md](docker/DOCKER_GUIDE.md)를 참조하세요.

### 방법 2: 로컬 개발 환경

#### 사전 요구사항

- **PostgreSQL**: 데이터베이스 서버
  - Windows: [공식 설치 프로그램](https://www.postgresql.org/download/windows/) 사용
  - Mac: `brew install postgresql@15` 또는 [Postgres.app](https://postgresapp.com/) 사용
  - Linux: `sudo apt-get install postgresql` (Ubuntu/Debian)
  - **또는 Docker**: `docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=fastapi_password postgres:15-alpine`

- **Redis**: 캐시 및 작업 큐
  - Windows: WSL 또는 Docker 권장
  - Mac: `brew install redis` 또는 Docker
  - Linux: `sudo apt-get install redis-server`
  - **또는 Docker**: `docker run -d -p 6379:6379 redis:7-alpine`

#### PostgreSQL 초기 설정

```bash
# PostgreSQL에 접속 (기본 superuser: postgres)
psql -U postgres

# 데이터베이스 생성
CREATE DATABASE fastapi_db;

# 사용자 생성 및 권한 부여
CREATE USER fastapi_user WITH PASSWORD 'fastapi_password';
ALTER ROLE fastapi_user SET client_encoding TO 'utf8';
ALTER ROLE fastapi_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE fastapi_user SET default_transaction_deferrable TO ON;
ALTER ROLE fastapi_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE fastapi_db TO fastapi_user;

# 연결 확인
\c fastapi_db fastapi_user

# 종료
\q
```

#### 의존성 설치

```bash
# uv를 사용하는 경우
uv pip install -e .

# 또는 pip를 사용하는 경우
pip install -e .
```

#### 개발 서버 실행

```bash
# 방법 1: main.py를 직접 실행
python app/main.py

# 방법 2: uvicorn을 직접 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```


### API 문서 확인

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:

- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## API 엔드포인트

### 기본 엔드포인트

- `GET /` - Welcome 메시지
- `GET /health` - 헬스 체크

### 인증 API (v1)

#### 회원가입
- `POST /api/v1/auth/register` - 새 사용자 등록

**요청:**
```bash
curl -X POST http://localhost:8001/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "name": "John Doe"
  }'
```

#### 로그인 (JWT 토큰 발급)
- `POST /api/v1/auth/login` - 사용자 로그인 및 JWT 토큰 획득

**요청:**
```bash
curl -X POST http://localhost:8001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

**응답:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 현재 사용자 정보 조회
- `GET /api/v1/auth/me` - 현재 로그인한 사용자 정보 조회 (Bearer 토큰 필요)

**요청:**
```bash
curl -X GET http://localhost:8001/api/v1/auth/me \
  -H "Authorization: Bearer {access_token}"
```

### Hello API (v1)

- `GET /api/v1/hello` - 기본 인사 메시지
- `GET /api/v1/hello/{name}` - 특정 이름에 대한 인사 메시지

### User API (v1)

- `POST /api/v1/users` - 새 사용자 생성 (관리자용)
- `GET /api/v1/users` - 모든 사용자 조회
- `GET /api/v1/users/{user_id}` - 특정 사용자 조회
- `PUT /api/v1/users/{user_id}` - 사용자 정보 수정 (본인만 가능, Bearer 토큰 필요)
- `DELETE /api/v1/users/{user_id}` - 사용자 삭제 (본인만 가능, Bearer 토큰 필요)

**사용자 생성 요청:**
```bash
curl -X POST http://localhost:8001/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "name": "John Doe"
  }'
```

**모든 사용자 조회:**
```bash
curl http://localhost:8001/api/v1/users
```

**특정 사용자 조회:**
```bash
curl http://localhost:8001/api/v1/users/1
```

**사용자 정보 수정 (Bearer 토큰 필요):**
```bash
curl -X PUT http://localhost:8001/api/v1/users/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {access_token}" \
  -d '{
    "name": "Updated Name"
  }'
```

**사용자 삭제 (Bearer 토큰 필요):**
```bash
curl -X DELETE http://localhost:8001/api/v1/users/1 \
  -H "Authorization: Bearer {access_token}"
```

## 디렉토리 구조 설명

### `app/core/`
- **config.py**: 환경 변수 관리 (Pydantic Settings)
- **database.py**: PostgreSQL 데이터베이스 엔진, 세션 관리
- **redis_queue.py**: Redis 연결, RQ 큐 설정

### `app/api/routes/`
- API 엔드포인트를 기능별로 분리
- APIRouter를 사용하여 라우트 정의
- `hello.py`: 기본 Hello API
- `users.py`: User CRUD API

### `app/models/`
- SQLModel을 사용한 데이터베이스 모델
- `user.py`: User 테이블 정의

### `app/schemas/`
- Pydantic 모델을 사용한 요청/응답 검증
- `user.py`: UserCreate, UserUpdate, UserResponse

### `app/services/`
- 비즈니스 로직 구현
- 데이터베이스 작업, 외부 API 호출 등
- 향후 Task 정의 위치

## 환경 변수

`.env` 파일에서 다음 변수들을 설정할 수 있습니다:

```dotenv
# Server Configuration
HOST=0.0.0.0
PORT=8001

# Application Configuration
PROJECT_NAME=Learning FastAPI
VERSION=0.1.0
DESCRIPTION=FastAPI Learning Project

# Database Configuration (PostgreSQL)
DATABASE_URL=postgresql://fastapi_user:fastapi_password@localhost:5432/fastapi_db

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=7379
REDIS_DB=0
REDIS_URL=redis://localhost:7379/0
```

## 데이터베이스

### PostgreSQL (주 데이터베이스)

프로덕션급 관계형 데이터베이스로 사용합니다.
- **Host**: localhost
- **Port**: 5432
- **Database**: fastapi_db
- **User**: fastapi_user
- **Password**: fastapi_password (`.env`에서 설정)

SQLModel을 통한 ORM 지원으로 안전하고 효율적인 데이터 관리가 가능합니다.

### User 모델

```python
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str  # Bcrypt로 해시된 패스워드
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### 데이터베이스 마이그레이션

**현재 프로젝트의 테이블 생성 방식:**
- 애플리케이션 시작 시 `SQLModel.metadata.create_all(engine)`을 통해 자동으로 테이블 생성
- 개발 단계에서는 간편하지만, 프로덕션에서는 제한적

**프로덕션 환경에서는 Alembic 사용 권장:**

```bash
# Alembic 설치
uv pip install alembic

# Alembic 초기화
alembic init alembic

# 마이그레이션 파일 생성
alembic revision --autogenerate -m "Create user table"

# 마이그레이션 적용
alembic upgrade head

# 마이그레이션 롤백
alembic downgrade -1
```

**서버 상시 운영 중 마이그레이션:**
1. 새로운 마이그레이션 파일 생성
2. 테스트 환경에서 마이그레이션 검증
3. 프로덕션 DB 백업
4. 마이그레이션 적용 (`alembic upgrade head`)
5. 애플리케이션 재시작 (다운타임 최소화를 위해 Blue-Green 배포 권장)

**Docker 환경에서의 마이그레이션:**

```bash
# 컨테이너 내부에서 실행
docker-compose exec app alembic upgrade head

# 또는 entrypoint에 추가하여 시작 시 자동 실행
```

## 보안 및 인증

### 패스워드 해싱

프로젝트는 **Bcrypt**를 사용하여 패스워드를 해싱합니다.

- **라이브러리**: `passlib[bcrypt]`
- **라운드**: 12 (Bcrypt 라운드 수, 기본값)
- **저장**: 데이터베이스에는 평문이 아닌 해시된 패스워드만 저장됨

**패스워드 해싱 및 검증 예:**
```python
from app.core.security import get_password_hash, verify_password

# 패스워드 해싱
hashed_password = get_password_hash("my_password")
# 결과: $2b$12$N9qo8uLOickgx2ZMRZoMye...

# 패스워드 검증
is_valid = verify_password("my_password", hashed_password)  # True
is_valid = verify_password("wrong_password", hashed_password)  # False
```

### JWT (JSON Web Token) 기반 인증

Bearer 토큰을 사용한 인증 구현:

**특징:**
- **토큰 생성**: 로그인 시 JWT 액세스 토큰 발급
- **토큰 검증**: API 요청 시 Bearer 토큰 검증
- **만료 시간**: 기본 30분 (`.env`에서 `ACCESS_TOKEN_EXPIRE_MINUTES` 설정)
- **알고리즘**: HS256 (HMAC SHA-256)
- **시크릿 키**: `SECRET_KEY` 환경 변수에서 관리

**Token 구조:**
```json
{
  "sub": "user@example.com",
  "exp": 1699999999
}
```

### 인증 흐름

```
1. 회원가입: POST /api/v1/auth/register
   ↓
2. 로그인: POST /api/v1/auth/login
   → JWT 액세스 토큰 반환
   ↓
3. 보호된 엔드포인트 요청: Authorization: Bearer {token}
   → 토큰 검증 후 현재 사용자 정보 제공
```

### Bearer 토큰 사용

**요청 헤더:**
```bash
Authorization: Bearer {access_token}
```

**curl 예제:**
```bash
curl -X GET http://localhost:8001/api/v1/auth/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 환경 변수 설정

`.env` 파일에 다음을 추가하세요:

```dotenv
# JWT Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**⚠️ 프로덕션 환경에서는 반드시:**
- `SECRET_KEY`를 강력한 무작위 문자열로 변경하세요
- 환경 변수를 통해 관리하세요
- HTTPS를 사용하세요

### 권한 제어 예제

현재 구현된 권한 제어:

1. **사용자 정보 수정**: 본인만 자신의 정보 수정 가능
2. **사용자 삭제**: 본인만 자신을 삭제 가능

관리자 권한 추가는 `User` 모델에 `is_admin` 필드를 추가하고 미들웨어를 통해 구현할 수 있습니다.

## Redis Queue (RQ)

### 사용 예시

```python
from app.core.redis_queue import default_queue, high_priority_queue
from app.services.tasks import send_email

# 기본 큐에 작업 추가
job = default_queue.enqueue(send_email, "user@example.com", "Hello")

# 높은 우선순위로 작업 추가
job = high_priority_queue.enqueue(send_email, "admin@example.com", "Important")

# 작업 상태 확인
print(job.get_status())  # queued, started, finished, failed
print(job.result)
```

### 사용 가능한 큐

- `default_queue`: 기본 우선순위
- `high_priority_queue`: 높은 우선순위
- `low_priority_queue`: 낮은 우선순위

## 추가 기능 확장

이 구조를 기반으로 다음과 같은 기능을 쉽게 추가할 수 있습니다:

- **고급 인증**: OAuth2 소셜 로그인 (Google, GitHub, Kakao)
- **역할 기반 접근 제어 (RBAC)**: 관리자, 일반 사용자 등 역할별 권한 관리
- **미들웨어**: CORS, 로깅, 속도 제한, 요청 추적
- **백그라운드 작업**: 이메일 발송, 데이터 처리, 스케줄 작업
- **파일 업로드**: S3, MinIO, local storage
- **테스트**: pytest, pytest-asyncio, 통합 테스트
- **캐싱 전략**: Redis 기반 자동 캐싱
- **데이터베이스 마이그레이션**: Alembic을 통한 버전 관리
- **API 버전 관리**: 다중 API 버전 지원
- **레이트 제한**: 사용자별, IP별 요청 제한
- **감시 및 로깅**: 구조화된 로깅, 에러 추적

## 참고 자료

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [SQLModel 공식 문서](https://sqlmodel.tiangolo.com/)
- [PostgreSQL 공식 문서](https://www.postgresql.org/docs/)
- [Redis 공식 문서](https://redis.io/)
- [RQ 공식 문서](https://python-rq.org/)
- [Docker Compose 공식 문서](https://docs.docker.com/compose/)
- [Alembic 마이그레이션 문서](https://alembic.sqlalchemy.org/)
- [python-jose JWT 문서](https://python-jose.readthedocs.io/)
- [Passlib 보안 라이브러리](https://passlib.readthedocs.io/)


