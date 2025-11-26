"""
Configuration Management Module
Loads environment variables and application settings
"""

from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    sentinel_client_id: Optional[str] = None
    sentinel_client_secret: Optional[str] = None
    usgs_api_key: Optional[str] = None
    
    # Application
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Data paths
    data_dir: Path = Path("data")
    imagery_dir: Path = Path("data/imagery")
    masks_dir: Path = Path("data/masks")
    cache_dir: Path = Path("data/cache")
    metadata_dir: Path = Path("data/metadata")
    
    # Model settings
    model_path: Optional[Path] = None
    use_precomputed_masks: bool = True
    pixel_resolution: float = 10.0
    
    # Processing
    max_tile_size: int = 1024
    min_building_size_pixels: int = 10
    default_overlay_alpha: float = 0.5
    
    # Logging
    log_level: str = "INFO"
    log_file: Path = Path("logs/asip.log")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
