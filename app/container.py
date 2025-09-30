from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from app.settings.server import ServerSettings


class AppContainer(DeclarativeContainer):
    """Контейнер с зависимостями."""

    server_settings: Singleton[ServerSettings] = Singleton(ServerSettings)
