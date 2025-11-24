from pydantic import BaseSettings


class Settings(BaseSettings):
    SENTINEL_HUB_API_KEY: str | None = None
    DEFAULT_IMAGERY_SOURCE: str = "static"
    DATA_DIR: str = "data"

    class Config:
        env_file = ".env"


settings = Settings()
