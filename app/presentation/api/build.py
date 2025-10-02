from fastapi import FastAPI

from app.presentation.api.routers import transcripts
from app.variables import PROJECT_VERSION

API_PREFIX = "/api"


def build_api(title: str) -> FastAPI:
    api = FastAPI(
        title=title,
        version=PROJECT_VERSION,
    )

    api.include_router(transcripts.router)

    return api
