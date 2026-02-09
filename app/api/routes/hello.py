from fastapi import APIRouter
from app.schemas.hello import HelloResponse

router = APIRouter()


@router.get("/hello/{name}", response_model=HelloResponse)
async def say_hello(name: str) -> HelloResponse:
    """Say hello to a specific name."""
    return HelloResponse(message=f"Hello {name}")


@router.get("/hello", response_model=HelloResponse)
async def say_hello_default() -> HelloResponse:
    """Say hello with default message."""
    return HelloResponse(message="Hello World")
