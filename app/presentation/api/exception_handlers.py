from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.presentation.api.schemas.common import ErrorResponseSchema


def add_exception_handlers(app: "FastAPI") -> None:
    app.add_exception_handler(Exception, unknown_error_handler)
    app.add_exception_handler(IntegrityError, conflict_error_handler)


def conflict_error_handler(_request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=ErrorResponseSchema(error_message=str(exc)).model_dump(),
    )


def unknown_error_handler(_request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponseSchema(error_message=str(exc)).model_dump(),
    )
