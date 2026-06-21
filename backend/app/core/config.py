from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_name: str = "Easy Hotel"
    environment: str = "development"
    database_url: str = "postgresql+psycopg://easy_hotel:easy_hotel@localhost:5432/easy_hotel"
    secret_key: str = "altere-esta-chave-em-producao"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    backend_cors_origins: str = Field(
        default="http://localhost:5173,http://127.0.0.1:5173,http://0.0.0.0:5173"
    )
    admin_default_name: str = "Administrador"
    admin_default_login: str = "admin"
    admin_default_password: str = "admin123"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.backend_cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
