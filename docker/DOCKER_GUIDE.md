# Docker Compose 실행 가이드

이 문서는 Docker Compose를 사용하여 FastAPI 애플리케이션을 실행하는 방법을 설명합니다.

## 전제 조건

- Docker 설치됨
- Docker Compose 설치됨
- Python 3.13 이상 (로컬 개발)

## 빠른 시작

### 0. 사전 준비

```bash
# 프로젝트 루트에서 docker 디렉토리로 이동
cd docker
```

### 1. 애플리케이션 시작

```bash
# 모든 서비스 시작 (백그라운드)
docker-compose up -d

# 모든 서비스 시작 (콘솔 로그 표시)
docker-compose up
```

### 2. API 확인

- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc
- Health Check: http://localhost:8001/health

### 3. 애플리케이션 중지

```bash
docker-compose down
```

## 서비스 설명

### app (FastAPI)
- **포트**: 8001
- **역할**: FastAPI 웹 서버
- **특징**: 자동 리로드 지원 (개발 환경)

### redis
- **포트**: 7379
- **역할**: 캐시 및 백그라운드 큐 브로커
- **데이터**: `redis_data` 볼륨에 저장

### worker (RQ Worker)
- **역할**: Redis Queue를 통한 백그라운드 작업 처리
- **큐**: default, high, low 3개 큐 모니터링

## 데이터베이스

- **타입**: SQLite
- **위치**: `./app.db`
- **볼륨**: `db_data` (Docker 볼륨)

## 자주 사용되는 명령어

```bash
# 로그 확인
docker-compose logs -f app

# 특정 서비스 재시작
docker-compose restart app

# 모든 서비스 재빌드 및 시작
docker-compose up -d --build

# 볼륨 포함 모든 것 제거
docker-compose down -v

# 서비스 상태 확인
docker-compose ps

# 컨테이너 내부 셸 접근
docker-compose exec app bash

# PostgreSQL 데이터베이스 초기화 (주의!)
docker-compose exec db psql -U fastapi_user -d fastapi_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
docker-compose restart app
```

## 환경 변수

프로젝트 루트의 `.env` 파일을 생성하여 다음 변수들을 설정할 수 있습니다:

또는 `docker` 디렉토리의 `.env.example`을 참고하여 설정할 수 있습니다:

```dotenv
HOST=0.0.0.0
PORT=8001
DATABASE_URL=postgresql://fastapi_user:fastapi_password@db:5432/fastapi_db
REDIS_HOST=redis
REDIS_PORT=7379
REDIS_URL=redis://localhost:7379/0
```

## 개발 워크플로우

### 로컬 개발 (Docker 미사용)

```bash
# uv를 사용한 의존성 설치
uv pip install -e .

# 또는 pip 사용
pip install -e .

# 서버 실행
python app/main.py

# 또는
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### Docker 개발

```bash
# 애플리케이션만 재빌드
docker-compose up -d --build app

# 최근 로그 100줄 확인
docker-compose logs --tail=100 -f
```

## Redis Queue (RQ) 사용 예제

### 백그라운드 작업 정의

```python
# app/services/tasks.py
def send_email(email: str, subject: str):
    """이메일 전송 (백그라운드 작업)."""
    # 실제 이메일 전송 로직
    pass

def process_image(image_path: str):
    """이미지 처리 (백그라운드 작업)."""
    # 이미지 처리 로직
    pass
```

### 큐에 작업 추가

```python
from app.core.redis_queue import default_queue, high_priority_queue
from app.services.tasks import send_email, process_image

# 기본 큐에 작업 추가
job = default_queue.enqueue(send_email, "user@example.com", "Hello")

# 높은 우선순위로 작업 추가
job = high_priority_queue.enqueue(process_image, "/path/to/image.jpg")

# 작업 상태 확인
print(job.get_status())
print(job.result)
```

## 문제 해결

### Redis 연결 실패

```bash
# Redis 상태 확인
docker-compose ps redis

# Redis 재시작
docker-compose restart redis

# Redis 로그 확인
docker-compose logs redis
```

### 데이터베이스 접근 권한 오류

```bash
# 컨테이너에서 권한 확인
docker-compose exec app ls -la app.db

# 볼륨 재생성
docker-compose down -v
docker-compose up -d
```

### 포트 충돌

포트 `8001`이 이미 사용 중인 경우:

```bash
# 환경 변수로 포트 변경
PORT=8002 docker-compose up -d
```

또는 `.env` 파일에서 `PORT` 값 변경:

```dotenv
PORT=8002
```

## 프로덕션 배포

프로덕션 환경에서는 다음을 권장합니다:

1. `.env` 파일 보안 관리
2. Gunicorn/Uvicorn 워커 수 증가
3. 리버스 프록시 (Nginx) 추가
4. PostgreSQL 백업 전략 수립
5. 볼륨 백업 및 복구 계획 수립


