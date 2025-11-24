from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    sentinel_instance_id: str = ""
    sentinel_client_id: str = ""
    sentinel_client_secret: str = ""

    class Config:
        env_file = ".env"  # reads from .env
        env_file_encoding = "utf-8"


settings = Settings()

# Optional: helpful paths
DATA_DIR = Path("data")
CACHE_DIR = DATA_DIR / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
