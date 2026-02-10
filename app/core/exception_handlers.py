"""예외 핸들러."""
import logging

from fastapi import Request, status
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """HTTP 예외 핸들러."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.error(
        f"HTTP Exception - Path: {request.url.path}, "
        f"RequestID: {request_id}, Error: {str(exc)}"
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal Server Error",
            "request_id": request_id,
        },
        headers={"X-Request-ID": request_id},
    )

