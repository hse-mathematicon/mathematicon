from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.variables import PROJECT_DIR


class DBSettings(BaseSettings):
    db_path: str

    @computed_field
    def url(self) -> str:
        return f"sqlite:///{Path(PROJECT_DIR, self.db_path).resolve()}"

    model_config = SettingsConfigDict(env_prefix="db_")
