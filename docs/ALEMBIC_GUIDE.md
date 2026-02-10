# Alembic 마이그레이션 가이드

## Alembic이란?

Alembic은 SQLAlchemy용 데이터베이스 마이그레이션 도구입니다. 데이터베이스 스키마 변경을 버전 관리하고 안전하게 적용할 수 있습니다.

## 설치

이미 프로젝트에 설치되어 있습니다:

```bash
pip install alembic
```

## 초기 설정 완료 사항

✅ Alembic 초기화 완료
✅ `alembic.ini` 설정 파일 생성
✅ `alembic/env.py` SQLModel과 연동
✅ 초기 마이그레이션 파일 생성 (001_initial_migration.py)

## 주요 명령어

### 1. 현재 마이그레이션 상태 확인

```bash
alembic current
```

### 2. 마이그레이션 히스토리 확인

```bash
alembic history --verbose
```

### 3. 마이그레이션 적용 (Upgrade)

```bash
# 최신 버전으로 업그레이드
alembic upgrade head

# 특정 버전으로 업그레이드
alembic upgrade 001

# 한 단계씩 업그레이드
alembic upgrade +1
```

### 4. 마이그레이션 되돌리기 (Downgrade)

```bash
# 한 단계 되돌리기
alembic downgrade -1

# 특정 버전으로 되돌리기
alembic downgrade 001

# 모두 되돌리기 (초기 상태)
alembic downgrade base
```

### 5. 새로운 마이그레이션 생성

#### 자동 생성 (권장)

모델 변경사항을 자동으로 감지하여 마이그레이션 생성:

```bash
alembic revision --autogenerate -m "Add user role column"
```

#### 수동 생성

빈 마이그레이션 파일 생성:

```bash
alembic revision -m "Custom migration"
```

### 6. 마이그레이션 정보 확인

```bash
# 현재 버전 확인
alembic current

# 다음 적용될 마이그레이션 확인
alembic show head

# 특정 마이그레이션 상세 정보
alembic show 001
```

## 워크플로우 예시

### 개발 환경 초기 설정

```bash
# 1. 최신 마이그레이션 적용
alembic upgrade head

# 2. 현재 상태 확인
alembic current
```

### 모델 변경 시

```bash
# 1. 모델 파일 수정 (예: app/api/users/models.py)
# User 모델에 새 필드 추가

# 2. 마이그레이션 자동 생성
alembic revision --autogenerate -m "Add phone_number to users"

# 3. 생성된 마이그레이션 파일 확인 및 수정 (필요시)
# alembic/versions/002_add_phone_number_to_users.py

# 4. 마이그레이션 적용
alembic upgrade head

# 5. 확인
alembic current
```

### 프로덕션 배포

```bash
# 1. 마이그레이션 파일을 git으로 커밋
git add alembic/versions/
git commit -m "Add migration: add phone_number to users"

# 2. 프로덕션 서버에서
# 2-1. 최신 코드 pull
git pull origin main

# 2-2. 마이그레이션 적용 (dry-run으로 먼저 확인)
alembic upgrade head --sql  # SQL만 출력

# 2-3. 실제 적용
alembic upgrade head

# 2-4. 확인
alembic current
```

## 마이그레이션 파일 구조

```python
"""Migration description

Revision ID: 001
Revises: None
Create Date: 2026-02-10
"""

def upgrade() -> None:
    """데이터베이스 업그레이드 로직."""
    # 테이블 생성
    op.create_table('users', ...)
    
    # 컬럼 추가
    op.add_column('users', sa.Column('phone', sa.String(20)))
    
    # 인덱스 생성
    op.create_index('idx_phone', 'users', ['phone'])


def downgrade() -> None:
    """롤백 로직."""
    op.drop_index('idx_phone', table_name='users')
    op.drop_column('users', 'phone')
    op.drop_table('users')
```

## 주요 작업 예시

### 1. 테이블 생성

```python
def upgrade():
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('content', sa.Text()),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now())
    )
```

### 2. 컬럼 추가

```python
def upgrade():
    op.add_column('users', sa.Column('phone_number', sa.String(20), nullable=True))
```

### 3. 컬럼 수정

```python
def upgrade():
    op.alter_column('users', 'name',
                    existing_type=sa.String(100),
                    type_=sa.String(200),
                    nullable=False)
```

### 4. 컬럼 삭제

```python
def upgrade():
    op.drop_column('users', 'old_column')
```

### 5. 인덱스 생성

```python
def upgrade():
    op.create_index('idx_email', 'users', ['email'], unique=True)
```

### 6. 외래 키 추가

```python
def upgrade():
    op.create_foreign_key(
        'fk_posts_user_id',
        'posts', 'users',
        ['user_id'], ['id'],
        ondelete='CASCADE'
    )
```

### 7. 데이터 마이그레이션

```python
def upgrade():
    # 새 컬럼 추가
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=True))
    
    # 기존 데이터 업데이트
    op.execute("UPDATE users SET is_active = true WHERE created_at < NOW()")
    
    # NOT NULL 제약조건 추가
    op.alter_column('users', 'is_active', nullable=False)
```

## 모범 사례

### ✅ DO

1. **항상 자동 생성 사용**: `--autogenerate` 사용
2. **마이그레이션 확인**: 생성된 파일을 항상 검토
3. **작은 단위로 나누기**: 각 마이그레이션은 하나의 논리적 변경만
4. **downgrade 작성**: 롤백 로직 항상 작성
5. **데이터 백업**: 프로덕션 적용 전 백업
6. **테스트**: 개발/스테이징 환경에서 먼저 테스트

### ❌ DON'T

1. **직접 SQL 실행 금지**: `SQLModel.metadata.create_all()` 대신 마이그레이션 사용
2. **마이그레이션 수정 금지**: 이미 적용된 마이그레이션은 수정하지 않음
3. **순서 건너뛰기 금지**: 마이그레이션은 순서대로 적용
4. **프로덕션 직접 적용 금지**: 항상 테스트 후 적용

## 트러블슈팅

### 문제: "Target database is not up to date"

**해결:**
```bash
# 현재 상태 확인
alembic current

# 마이그레이션 적용
alembic upgrade head
```

### 문제: 마이그레이션 충돌

**해결:**
```bash
# 충돌 확인
alembic history

# 수동으로 마이그레이션 파일 수정
# down_revision을 올바르게 설정
```

### 문제: 자동 생성이 변경사항을 감지하지 못함

**해결:**
1. 모든 모델이 `alembic/env.py`에 import되었는지 확인
2. `SQLModel.metadata`가 올바르게 설정되었는지 확인
3. 모델 파일에 syntax 에러가 없는지 확인

## 환경별 설정

### 개발 환경

```bash
# .env
DATABASE_URL=postgresql://user:pass@localhost:5432/dev_db

# 마이그레이션 자유롭게 테스트
alembic upgrade head
alembic downgrade -1
alembic upgrade head
```

### 스테이징 환경

```bash
# .env
DATABASE_URL=postgresql://user:pass@staging-host:5432/staging_db

# 프로덕션 배포 전 최종 테스트
alembic upgrade head
```

### 프로덕션 환경

```bash
# .env
DATABASE_URL=postgresql://user:pass@prod-host:5432/prod_db

# 백업 후 신중하게 적용
pg_dump prod_db > backup_$(date +%Y%m%d).sql
alembic upgrade head
```

## 통합: FastAPI와 Alembic

### app/main.py 수정

```python
# 개발 환경에서만 자동 테이블 생성 (선택사항)
if settings.ENVIRONMENT == "development":
    create_db_and_tables()
else:
    # 프로덕션에서는 Alembic 사용 강제
    logger.info("Use 'alembic upgrade head' to apply migrations")
```

### 배포 스크립트

```bash
#!/bin/bash
# deploy.sh

echo "Pulling latest code..."
git pull origin main

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
alembic upgrade head

echo "Restarting application..."
systemctl restart fastapi-app

echo "Deployment complete!"
```

## 추가 리소스

- [Alembic 공식 문서](https://alembic.sqlalchemy.org/)
- [SQLAlchemy 문서](https://docs.sqlalchemy.org/)
- [FastAPI + Alembic 예제](https://fastapi.tiangolo.com/tutorial/sql-databases/)

## 다음 단계

1. `alembic upgrade head` 실행하여 초기 마이그레이션 적용
2. User 모델 변경 시 새 마이그레이션 생성
3. 팀원들과 마이그레이션 워크플로우 공유
4. CI/CD 파이프라인에 마이그레이션 통합

