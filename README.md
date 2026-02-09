# FastAPI Learning Project

이 프로젝트는 FastAPI의 대중적인 디렉토리 구조를 따릅니다.

## 프로젝트 구조

```
learning/
├── app/                    # 메인 애플리케이션 패키지
│   ├── __init__.py
│   ├── main.py            # FastAPI 앱 인스턴스 및 라우터 설정
│   ├── api/               # API 관련 코드
│   │   ├── __init__.py
│   │   └── routes/        # API 라우트 모듈
│   │       ├── __init__.py
│   │       └── hello.py   # Hello 엔드포인트
│   ├── core/              # 핵심 설정 및 유틸리티
│   │   ├── __init__.py
│   │   └── config.py      # 설정 관리 (환경 변수 등)
│   ├── models/            # 데이터베이스 모델 (SQLAlchemy 등)
│   │   └── __init__.py
│   ├── schemas/           # Pydantic 스키마 (요청/응답 검증)
│   │   ├── __init__.py
│   │   └── hello.py
│   └── services/          # 비즈니스 로직
│       └── __init__.py
├── main.py                # 애플리케이션 진입점
├── pyproject.toml         # 프로젝트 의존성 및 설정
└── test_main.http         # HTTP 테스트 파일
```

## 설치 및 실행

### 의존성 설치

```bash
# uv를 사용하는 경우
uv pip install -e .

# 또는 pip를 사용하는 경우
pip install -e .
```

### 개발 서버 실행

```bash
# 방법 1: main.py를 직접 실행
python main.py

# 방법 2: uvicorn을 직접 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### API 문서 확인

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 엔드포인트

### 기본 엔드포인트

- `GET /` - Welcome 메시지
- `GET /health` - 헬스 체크

### Hello API (v1)

- `GET /api/v1/hello` - 기본 인사 메시지
- `GET /api/v1/hello/{name}` - 특정 이름에 대한 인사 메시지

## 디렉토리 구조 설명

### `app/core/`
- 애플리케이션 설정, 환경 변수 관리
- 보안, 인증 관련 유틸리티
- 공통 미들웨어

### `app/api/routes/`
- API 엔드포인트를 기능별로 분리
- 각 파일은 APIRouter를 사용하여 라우트 정의

### `app/schemas/`
- Pydantic 모델을 사용한 요청/응답 스키마
- 데이터 검증 및 직렬화

### `app/models/`
- SQLAlchemy 또는 다른 ORM 모델
- 데이터베이스 테이블 정의

### `app/services/`
- 비즈니스 로직 구현
- 데이터베이스 작업, 외부 API 호출 등

## 환경 변수

`.env` 파일을 생성하여 환경 변수를 설정할 수 있습니다. `.env.example`을 참조하세요.

## 추가 기능 확장

이 구조를 기반으로 다음과 같은 기능을 쉽게 추가할 수 있습니다:

- 데이터베이스 연동 (SQLAlchemy, Tortoise ORM 등)
- 인증/인가 (JWT, OAuth2)
- 미들웨어 (CORS, 로깅 등)
- 백그라운드 태스크 (Celery, Redis Queue)
- 테스트 (pytest, pytest-asyncio)
