from pathlib import Path

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton
from dotenv import load_dotenv

from app.settings import ServerSettings
from app.variables import PROJECT_DIR

load_dotenv(Path(PROJECT_DIR, ".env"))


class AppContainer(DeclarativeContainer):
    """Контейнер с зависимостями."""

    # Settings
    server_settings: Singleton[ServerSettings] = Singleton(ServerSettings)
