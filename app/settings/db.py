from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.variables import PROJECT_DIR


class DBSettings(BaseSettings):
    db_path: str

    @property
    def url(self) -> str:
        return f"sqlite:///{Path(PROJECT_DIR, self.db_path).resolve()}"

    model_config = SettingsConfigDict(env_prefix="db_")
