from fastapi import FastAPI

from app.presentation.api.routers import grammar_annotation, transcripts
from app.variables import PROJECT_VERSION

API_PREFIX = "/api"


def build_api(title: str) -> FastAPI:
    api = FastAPI(
        title=title,
        version=PROJECT_VERSION,
    )

    api.include_router(transcripts.router)
    api.include_router(grammar_annotation.router)

    return api
