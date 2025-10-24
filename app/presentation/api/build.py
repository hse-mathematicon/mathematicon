from fastapi import FastAPI

from app.presentation.api.exception_handlers import add_exception_handlers
from app.presentation.api.routers import grammar_annotation, math_ontology, transcripts, morphology
from app.variables import PROJECT_VERSION

API_PREFIX = "/api"


def build_api(title: str) -> FastAPI:
    api = FastAPI(
        title=title,
        version=PROJECT_VERSION,
    )

    api.include_router(transcripts.router)
    api.include_router(grammar_annotation.router)
    api.include_router(math_ontology.router)
    api.include_router(morphology.router)

    add_exception_handlers(api)

    return api
