from fastapi import FastAPI

API_PREFIX = "/api"


def build_api(title: str, version: str) -> FastAPI:
    api = FastAPI(
        title=title,
        version=version,
    )
    return api