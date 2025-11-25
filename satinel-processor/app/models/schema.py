from pydantic import BaseModel
from typing import List, Optional, Dict


class BuildingStats(BaseModel):
    count: int = 0
    total_footprint_area: float = 0.0  # placeholder square meters
    density_per_km2: float = 0.0


class ChangeStats(BaseModel):
    new: int = 0
    removed: int = 0
    activity_score: float = 0.0


class TaskRequest(BaseModel):
    task_id: Optional[str] = None
    area_id: Optional[str] = None  # either area_id or lat/lon may be provided
    lat: Optional[float] = None
    lon: Optional[float] = None
    date: Optional[str] = None
    imagery_source: Optional[str] = None  # e.g. sentinel|usgs|static


class BatchRequest(BaseModel):
    tasks: List[TaskRequest]


class TaskResponse(BaseModel):
    task_id: str
    status: str
    source: Optional[str] = None  # which imagery source was used
    building_stats: Optional[BuildingStats] = None
    change_stats: Optional[ChangeStats] = None
    results: Optional[Dict] = None  # raw / additional data
