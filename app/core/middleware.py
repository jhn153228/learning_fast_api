"""미들웨어 설정."""
import time
import uuid
from contextvars import ContextVar
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# Request ID를 저장하는 컨텍스트 변수
request_id_var: ContextVar[str] = ContextVar("request_id", default="")


class RequestIDMiddleware(BaseHTTPMiddleware):
    """모든 요청에 고유한 Request ID를 추가하는 미들웨어."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # 클라이언트가 제공한 Request ID 사용, 없으면 생성
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request_id_var.set(request_id)

        # Request 객체에 request_id 추가
        request.state.request_id = request_id

        response = await call_next(request)

        # 응답 헤더에 Request ID 추가
        response.headers["X-Request-ID"] = request_id

        return response


class ResponseTimeMiddleware(BaseHTTPMiddleware):
    """응답 시간을 측정하고 헤더에 추가하는 미들웨어."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = f"{process_time:.4f}"

        return response


def get_request_id() -> str:
    """현재 요청의 Request ID를 반환."""
    return request_id_var.get()

