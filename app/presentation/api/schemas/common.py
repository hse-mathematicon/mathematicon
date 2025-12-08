from typing import Generic, TypeVar, Union

from pydantic import BaseModel

ResponseT = TypeVar("ResponseT")


class ErrorResponseSchema(BaseModel):
    error_message: str


class WarningSchema(BaseModel):
    detail: str


class OperationResultSchema(BaseModel, Generic[ResponseT]):
    data: Union[ResponseT, None] = None
    warnings: list[WarningSchema]
