from pydantic import BaseModel


class ErrorResponseSchema(BaseModel):
    error_message: str
