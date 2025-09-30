from fastapi import FastAPI

API_PREFIX = "/api"


def build_api(title: str, version: str) -> FastAPI:
    return FastAPI(
        title=title,
        version=version,
    )
