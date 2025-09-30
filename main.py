from importlib import metadata

from fastapi import FastAPI
import uvicorn

from app.container import AppContainer
from app.presentation.api.build import build_api, API_PREFIX


def create_app() -> FastAPI:
    version = metadata.version("mathematicon")

    app = FastAPI(
        docs_url=None,
        redoc_url=None,
    )
    app.mount(API_PREFIX, build_api(title="Mathematicon API", version=version))
    return app


if __name__ == '__main__':
    container = AppContainer()
    container.wire(packages=["app"])
    uvicorn.run("main:create_app", **container.server_settings().model_dump())
