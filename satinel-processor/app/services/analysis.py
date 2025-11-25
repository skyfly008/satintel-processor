import asyncio
from pathlib import Path
from typing import List, Optional
from PIL import Image

from ..models.schema import TaskRequest, TaskResponse, BatchRequest, BuildingStats, ChangeStats
from satinel.api_fetch import fetch_dynamic_imagery
from satinel.imagery_io import load_image
from satinel.data_config import snap_to_aoi_tile


async def process_task(req: TaskRequest) -> TaskResponse:
    """Basic task processing:
    1. Resolve area_id (either provided or snapped from lat/lon)
    2. Fetch or fallback to static imagery path
    3. Load image and compute dummy stats (pixel dimensions -> area proxy)
    4. Return TaskResponse with placeholder BuildingStats and ChangeStats
    
    Supports mode via req.imagery_source:
    - 'dynamic': Try Sentinel/USGS live fetch with cache
    - 'static' or None: Use pre-stored imagery
    """
    # Resolve area
    area_id = req.area_id
    if area_id is None and req.lat is not None and req.lon is not None:
        area_id = snap_to_aoi_tile(req.lon, req.lat) or "AREA_1"  # default fallback

    date = req.date or "2023-01-01"
    mode = req.imagery_source or "static"

    # Fetch imagery path
    if mode == "dynamic":
        # Pass lat/lon to fetch_dynamic_imagery for 512x512 clips around point
        path = fetch_dynamic_imagery(area_id, date, lat=req.lat, lon=req.lon)
    else:
        # Static mode: use pre-stored imagery (or fetch without lat/lon for AOI-based)
        path = fetch_dynamic_imagery(area_id, date)

    width = height = 0
    try:
        img = load_image(path)
        width, height = img.size
    except Exception:
        # If image missing, keep zeros; caller can inspect results
        pass

    # Dummy building stats (using pixel area as placeholder)
    pixel_area = width * height
    building_stats = BuildingStats(
        count=0,
        total_footprint_area=float(pixel_area),
        density_per_km2=0.0,
    )

    change_stats = ChangeStats()  # all zeros placeholder

    results = {
        "area_id": area_id,
        "date": date,
        "mode": mode,
        "pixel_width": width,
        "pixel_height": height,
        "pixel_area": pixel_area,
        "imagery_path": path,
    }

    task_id = req.task_id or f"{area_id}:{date}"
    return TaskResponse(
        task_id=task_id,
        status="done",
        source=mode,
        building_stats=building_stats,
        change_stats=change_stats,
        results=results,
    )


async def process_batch(req: BatchRequest) -> List[TaskResponse]:
    tasks = [process_task(t) for t in req.tasks]
    return await asyncio.gather(*tasks)


def process_task_coords(lat: float, lon: float, date: Optional[str] = None) -> TaskResponse:
    """Synchronous convenience wrapper for manual shell testing.
    Example: process_task_coords(35.0, -97.0, None)
    """
    loop = asyncio.get_event_loop()
    treq = TaskRequest(lat=lat, lon=lon, date=date)
    return loop.run_until_complete(process_task(treq))
