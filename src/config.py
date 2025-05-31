from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    directory_path: str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# @lru_cache()
def get_settings():
    return Settings()
