from fastapi import FastAPI
import uvicorn

from app.container import AppContainer
from app.presentation.api.build import build_api, API_PREFIX

container = AppContainer()
container.wire(packages=["app"])


def create_app() -> FastAPI:

    app = FastAPI(
        docs_url=None,
        redoc_url=None,
    )

    app.mount(API_PREFIX, build_api(title="Mathematicon API"))

    return app


if __name__ == '__main__':
    uvicorn.run(**container.server_settings().model_dump())
