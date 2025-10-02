from pathlib import Path

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton
from dotenv import load_dotenv
from sqlalchemy.engine import Engine, create_engine

from app.settings import DBSettings, ServerSettings
from app.variables import PROJECT_DIR

load_dotenv(Path(PROJECT_DIR, ".env"))


class AppContainer(DeclarativeContainer):
    """Контейнер с зависимостями."""

    # Settings
    server_settings: Singleton[ServerSettings] = Singleton(ServerSettings)
    db_settings: Singleton[DBSettings] = Singleton(DBSettings)

    # Database
    engine: Singleton[Engine] = Singleton(create_engine, url=db_settings.provided.url)
