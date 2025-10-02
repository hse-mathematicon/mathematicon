from fastapi import FastAPI

from app.variables import PROJECT_VERSION

API_PREFIX = "/api"


def build_api(title: str) -> FastAPI:
    return FastAPI(
        title=title,
        version=PROJECT_VERSION,
    )
