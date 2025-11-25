from pydantic import BaseModel
from typing import List, Optional, Dict


class BuildingStats(BaseModel):
    count: int = 0
    total_footprint_area: float = 0.0  # in square meters
    density_per_km2: float = 0.0


class ChangeStats(BaseModel):
    new: int = 0
    removed: int = 0
    unchanged: int = 0
    activity_score: float = 0.0  # scale 0-100
    temporal_change_pct: float = 0.0


class TaskRequest(BaseModel):
    task_id: Optional[str] = None
    area_id: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    date: Optional[str] = None
    historical_date: Optional[str] = None  # for temporal comparison
    imagery_source: Optional[str] = None  # sentinel, usgs, or static


class BatchRequest(BaseModel):
    tasks: List[TaskRequest]


class TaskResponse(BaseModel):
    task_id: str
    status: str
    source: Optional[str] = None
    building_stats: Optional[BuildingStats] = None
    change_stats: Optional[ChangeStats] = None
    overlay_url: Optional[str] = None
    results: Optional[Dict] = None
