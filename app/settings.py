from typing import List
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    origins: str
    host_path: str
    directory_path: str
    chunk_size: int

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def allow_origins(self) -> List[str]:
        if self.origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.origins.split(",") if origin.strip()]


@lru_cache()
def get_settings():
    return Settings()
