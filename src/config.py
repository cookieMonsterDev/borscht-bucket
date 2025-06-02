from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    base_path: str
    chunk_size: int
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# @lru_cache()
def get_settings():
    return Settings()
