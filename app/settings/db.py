from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.variables import PROJECT_DIR


class DBSettings(BaseSettings):
    file_path: str

    @property
    def url(self) -> str:
        return f"sqlite:///{Path(PROJECT_DIR, self.file_path).resolve()}"

    model_config = SettingsConfigDict(env_prefix="db_")
