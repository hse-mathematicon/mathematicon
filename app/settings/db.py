from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.variables import PROJECT_DIR


class DBSettings(BaseSettings):
    db_path: str = "data/mathematicon.db"

    @property
    def url(self) -> str:
        # Принудительно создаем базу если не существует
        db_file = Path(PROJECT_DIR, self.db_path)
        db_file.parent.mkdir(exist_ok=True)
        if not db_file.exists():
            import sqlite3
            sqlite3.connect(db_file).close()
            print(f"Создана база данных: {db_file}")
            
        return f"sqlite:///{db_file.resolve()}"

    model_config = SettingsConfigDict(env_prefix="db_")
