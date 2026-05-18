from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Base de datos
    database_url: str
    AEMET_API_KEY: str = ""
    AEMET_MUNICIPIO: str = "28029"
    # JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 480
    supabase_url: str = ""
    supabase_key: str = ""
    # CORS
    allowed_origins: str = "http://localhost:4200"

    # Entorno
    environment: str = "development"

    @property
    def origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
