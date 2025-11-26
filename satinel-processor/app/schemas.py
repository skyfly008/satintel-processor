"""
Pydantic Schemas - Request/Response models for API.

Defines data validation and serialization models for:
- Task requests
- Analysis results
- Change detection results
- Statistics
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime


class TaskRequest(BaseModel):
    """Request model for satellite tasking - current date only."""
    
    lat: float = Field(..., description="Latitude", ge=-90, le=90)
    lon: float = Field(..., description="Longitude", ge=-180, le=180)
    area_id: Optional[str] = Field(None, description="Specific area ID if known")


class BuildingStats(BaseModel):
    """Building statistics model."""
    
    building_count: int = Field(..., description="Total number of buildings detected")
    built_area_km2: float = Field(..., description="Total built area in square kilometers")
    density_per_km2: float = Field(..., description="Building density per km²")
    avg_building_size_m2: Optional[float] = Field(None, description="Average building size")
    largest_building_m2: Optional[float] = Field(None, description="Largest building size")


class TaskResponse(BaseModel):
    """Response model for completed task analysis - current state only."""
    
    area_id: str = Field(..., description="Area identifier")
    date: str = Field(..., description="Analysis date (current)")
    lat: float = Field(..., description="Actual latitude used")
    lon: float = Field(..., description="Actual longitude used")
    
    # Image URLs
    image_url: str = Field(..., description="URL to base satellite image")
    overlay_url: str = Field(..., description="URL to building overlay image")
    
    # Analysis results
    stats: BuildingStats = Field(..., description="Building statistics")
    
    # Metadata
    tile_size_km: float = Field(..., description="Tile coverage in km²")
    resolution_m: float = Field(..., description="Image resolution in meters per pixel")
    processing_time_ms: Optional[int] = Field(None, description="Processing time in milliseconds")


class AreaInfo(BaseModel):
    """Information about an available area."""
    
    area_id: str = Field(..., description="Area identifier")
    name: str = Field(..., description="Human-readable area name")
    center_lat: float = Field(..., description="Area center latitude")
    center_lon: float = Field(..., description="Area center longitude")
    tile_count: int = Field(..., description="Number of available tiles")


class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    areas_available: int = Field(..., description="Number of areas with imagery")
