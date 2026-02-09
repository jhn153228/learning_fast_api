from pydantic import BaseModel


class HelloResponse(BaseModel):
    """Response schema for hello endpoints."""

    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Hello World"
            }
        }
