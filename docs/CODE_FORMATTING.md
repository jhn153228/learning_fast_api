# 코드 포맷팅 및 린팅 가이드

## 설치된 도구

- **Ruff**: 초고속 Python 린터 및 포매터 (Black, Flake8, isort를 모두 대체)
- **mypy**: 정적 타입 체킹

---

## Ruff 설정 (현대적 표준)

### 주요 설정값

```toml
[tool.ruff]
line-length = 88              # 한 줄 최대 길이 (Black 호환)
target-version = "py313"      # Python 버전 타겟

[tool.ruff.lint]
select = ["E", "W", "F", "I", "UP", "B", "C4", "SIM"]
ignore = ["E501"]             # line-too-long (formatter가 처리)

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### 특징
- **⚡ 10-100배 빠름**: Rust로 작성되어 Black/Flake8/isort보다 훨씬 빠름
- **올인원**: 린터 + 포매터 + import 정렬을 하나의 도구로
- **Black 호환**: Black과 동일한 포맷팅 결과
- **700+ 규칙**: Flake8, pylint, pyupgrade 등의 규칙 통합

---

## 사용 방법

### 1. 전체 프로젝트 포맷팅 및 린팅

```bash
# 린팅 (코드 품질 검사)
ruff check app/

# 자동 수정 가능한 문제 수정
ruff check --fix app/

# 포맷팅 (코드 스타일 정리)
ruff format app/

# 한 번에 실행 (린팅 + 포맷팅)
ruff check --fix app/ && ruff format app/
```

### 2. 특정 파일 포맷팅

```bash
# 특정 파일만 포맷팅
ruff format app/main.py

# 특정 파일만 린팅
ruff check app/main.py
```

### 3. 검사만 하기 (변경하지 않음)

```bash
# 린팅 검사만
ruff check app/

# 포맷팅 검사만
ruff format --check app/

# mypy 타입 체크
mypy app/
```

### 4. 차이점 확인

```bash
# 린팅 수정 사항 미리보기
ruff check --diff app/

# 포맷팅 변경 내용 미리보기
ruff format --diff app/
```

---

## VS Code 설정

`.vscode/settings.json` 파일 생성:

```json
{
  "[python]": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll": true,
      "source.organizeImports": true
    },
    "editor.defaultFormatter": "charliermarsh.ruff"
  },
  "ruff.enable": true,
  "ruff.lint.enable": true,
  "ruff.format.enable": true,
  "python.linting.enabled": false,  // Ruff가 대체
  "python.formatting.provider": "none",  // Ruff가 대체
  "python.analysis.typeCheckingMode": "basic"
}
```

**필수 확장**: Ruff 확장 설치
- VS Code에서 `charliermarsh.ruff` 검색 후 설치

---

## PyCharm/JetBrains 설정

1. **Settings** → **Tools** → **Ruff**
   - Ruff 경로 설정
   - "Run ruff on save" 체크

2. **Settings** → **Editor** → **Code Style** → **Python**
   - Formatter를 "Ruff"로 설정

---

## Pre-commit Hook (권장)

`.pre-commit-config.yaml` 파일:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      # 린터로 실행
      - id: ruff
        args: [--fix]
      # 포매터로 실행
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

설치:
```bash
pip install pre-commit
pre-commit install
```

---

## 실전 워크플로우

### 개발 중

```bash
# 1. 코드 작성
# 2. 저장 시 자동 포맷팅 및 린팅 (VS Code 설정 시)
```

### 커밋 전

```bash
# 전체 포맷팅 및 검사
ruff check --fix app/
ruff format app/
mypy app/
```

### CI/CD 파이프라인

```yaml
# .github/workflows/lint.yml
name: Lint

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.13'
      - name: Install dependencies
        run: |
          pip install ruff mypy
      - name: Lint with Ruff
        run: ruff check app/
      - name: Check formatting with Ruff
        run: ruff format --check app/
      - name: Type check with mypy
        run: mypy app/
```

---

## 주요 Ruff 규칙

### 1. 문자열 따옴표
```python
# Ruff는 큰따옴표(") 선호 (Black 호환)
name = "John"  # ✅
name = 'John'  # ❌ (자동으로 " 로 변경)
```

### 2. 함수 매개변수 정렬
```python
# Before
def function(arg1, arg2, arg3, arg4, arg5, arg6, arg7):
    pass

# After (88자 초과 시)
def function(
    arg1,
    arg2,
    arg3,
    arg4,
    arg5,
    arg6,
    arg7,
):
    pass
```

### 3. Import 정리 (자동)
```python
# Ruff가 자동으로 정렬 및 그룹화
# 표준 라이브러리
import os
import sys

# 서드파티
from fastapi import FastAPI

# 로컬
from app.core.config import settings
```

### 4. 코드 품질 규칙
```python
# 사용하지 않는 import 자동 제거
# 사용하지 않는 변수 경고
# 비효율적인 코드 패턴 개선 제안
```

---

## Ruff 규칙 카테고리

- **E, W**: pycodestyle (PEP 8 스타일)
- **F**: Pyflakes (논리적 오류)
- **I**: isort (import 정렬)
- **UP**: pyupgrade (Python 버전 업그레이드)
- **B**: flake8-bugbear (버그 가능성)
- **C4**: flake8-comprehensions (list/dict comprehension)
- **SIM**: flake8-simplify (코드 단순화)

---

## 자주 묻는 질문 (FAQ)

### Q: Ruff가 Black/Flake8보다 나은 이유는?
**A**: 
- **속도**: Rust로 작성되어 10-100배 빠름
- **통합**: 여러 도구를 하나로 통합
- **호환성**: Black과 100% 호환되는 포맷팅
- **확장성**: 700개 이상의 린팅 규칙

### Q: 기존 Black 프로젝트에서 전환하기 쉬운가요?
**A**: 매우 쉽습니다. Ruff는 Black과 호환되도록 설계되었습니다:
```bash
# Black 대체
ruff format app/

# Black + isort + flake8 대체
ruff check --fix app/ && ruff format app/
```

### Q: 기존 코드에 적용하려면?
**A**: 
```bash
# 전체 프로젝트에 한 번에 적용
ruff check --fix app/
ruff format app/

# 변경사항 확인 후 커밋
git diff
git add -A
git commit -m "style: Apply Ruff formatting and linting"
```

### Q: 특정 규칙을 무시하려면?
**A**: 
```python
# 파일 전체에서 무시
# ruff: noqa: E501

# 특정 줄만 무시
x = "very long string"  # noqa: E501

# 여러 규칙 무시
# noqa: E501, F401
```

---

## 베스트 프랙티스

### ✅ 권장사항

1. **프로젝트 시작부터 적용**: 초기부터 Ruff 사용
2. **팀 전체 적용**: 모든 개발자가 동일한 설정 사용
3. **자동화**: pre-commit hook 또는 CI/CD 통합
4. **저장 시 포맷팅**: IDE 설정으로 자동 실행
5. **정기 업데이트**: Ruff는 빠르게 발전 중

### ❌ 피해야 할 것

1. `# noqa` 주석을 남발
2. 수동 포맷팅 (시간 낭비)
3. 팀원마다 다른 설정
4. Ruff와 Black/Flake8을 동시 사용 (중복)

---

## 유용한 명령어 모음

```bash
# 모든 Python 파일 린팅
ruff check .

# 자동 수정 가능한 것 모두 수정
ruff check --fix .

# 모든 Python 파일 포맷팅
ruff format .

# 특정 디렉토리만
ruff check app/api/
ruff format app/api/

# 변경하지 않고 검사만
ruff check .
ruff format --check .

# 변경될 내용 미리보기
ruff check --diff .
ruff format --diff .

# 통계 보기
ruff check --statistics .

# 한 줄로 전체 검사
ruff check . && ruff format --check . && mypy .

# 린팅 + 포맷팅 + 타입 체크 (전체 워크플로우)
ruff check --fix . && ruff format . && mypy .
```

---

## Ruff vs Black/Flake8/isort 비교

| 기능 | Ruff | Black + Flake8 + isort |
|------|------|------------------------|
| 포맷팅 | ✅ | ✅ (Black) |
| 린팅 | ✅ | ✅ (Flake8) |
| Import 정렬 | ✅ | ✅ (isort) |
| 속도 | ⚡⚡⚡ (초고속) | 🐌 (느림) |
| 설치 | 1개 패키지 | 3개 패키지 |
| 설정 | 1개 파일 | 3개 파일 |
| 유지보수 | 쉬움 | 복잡함 |

---

## 참고 자료

- [Ruff 공식 문서](https://docs.astral.sh/ruff/)
- [Ruff GitHub](https://github.com/astral-sh/ruff)
- [Ruff 규칙 목록](https://docs.astral.sh/ruff/rules/)
- [PEP 8 스타일 가이드](https://peps.python.org/pep-0008/)
- [mypy 문서](https://mypy.readthedocs.io/)

---

**작성일**: 2026-02-10  
**버전**: 2.0.0 (Ruff 전환)

