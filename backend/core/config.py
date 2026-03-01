from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "SRPP Studio Backend"
    environment: str = "development"
    mongo_url: str
    groq_api_key: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()