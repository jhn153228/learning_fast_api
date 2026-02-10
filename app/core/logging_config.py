"""로깅 설정."""
import logging
import sys
from pathlib import Path

from app.core.middleware import get_request_id


class RequestIDFilter(logging.Filter):
    """로그에 Request ID를 추가하는 필터."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = get_request_id() or "no-request-id"
        return True


def setup_logging():
    """로깅 설정을 초기화."""
    # 로그 디렉토리 생성
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # 로그 포맷 설정
    log_format = (
        "%(asctime)s - %(name)s - %(levelname)s - "
        "[RequestID: %(request_id)s] - %(message)s"
    )

    # 루트 로거 설정
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # 콘솔 핸들러
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(log_format)
    console_handler.setFormatter(console_formatter)
    console_handler.addFilter(RequestIDFilter())

    # 파일 핸들러
    file_handler = logging.FileHandler(log_dir / "app.log", encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(log_format)
    file_handler.setFormatter(file_formatter)
    file_handler.addFilter(RequestIDFilter())

    # 에러 파일 핸들러
    error_handler = logging.FileHandler(log_dir / "error.log", encoding="utf-8")
    error_handler.setLevel(logging.ERROR)
    error_formatter = logging.Formatter(log_format)
    error_handler.setFormatter(error_formatter)
    error_handler.addFilter(RequestIDFilter())

    # 기존 핸들러 제거 후 새 핸들러 추가
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_handler)

    # uvicorn 로거 설정
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.handlers.clear()
    uvicorn_logger.addHandler(console_handler)
    uvicorn_logger.addHandler(file_handler)

    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.handlers.clear()
    uvicorn_access_logger.addHandler(console_handler)
    uvicorn_access_logger.addHandler(file_handler)

    return root_logger


# 로거 인스턴스
logger = logging.getLogger(__name__)

