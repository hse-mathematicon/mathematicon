from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseSettings):
    host: str = '0.0.0.0'
    port: int = 8000
    reload: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_prefix="server_")