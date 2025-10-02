from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseSettings):
    app: str = "main:create_app"
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False
    factory: bool = True
    log_level: str = "info"

    model_config = SettingsConfigDict(env_prefix="server_")
