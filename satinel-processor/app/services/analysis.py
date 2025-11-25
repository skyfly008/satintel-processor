import asyncio
from pathlib import Path
from typing import List, Optional
from PIL import Image
import numpy as np

from ..models.schema import TaskRequest, TaskResponse, BatchRequest, BuildingStats, ChangeStats
from satinel.api_fetch import fetch_dynamic_imagery
from satinel.imagery_io import load_image
from satinel.data_config import snap_to_aoi_tile, get_aoi
from satinel.object_model import detect_objects


def compute_building_stats(detections: List[dict], aoi_area_km2: float = 1.0) -> BuildingStats:
    """Compute building statistics from SAM detections.
    
    Args:
        detections: List of detection dicts with 'area' in pixels
        aoi_area_km2: Area of interest in km for density calculation
    
    Returns:
        BuildingStats with count, total area, and density
    """
    if not detections:
        return BuildingStats(count=0, total_footprint_area=0.0, density_per_km2=0.0)
    
    count = len(detections)
    # Assuming 10m/pixel resolution (Sentinel-2), convert pixel area to m
    PIXEL_AREA_M2 = 10 * 10  # 100 m per pixel
    total_area_m2 = sum(det.get("area", 0) * PIXEL_AREA_M2 for det in detections)
    density = count / aoi_area_km2 if aoi_area_km2 > 0 else 0.0
    
    return BuildingStats(
        count=count,
        total_footprint_area=total_area_m2,
        density_per_km2=density,
    )


async def process_task(req: TaskRequest) -> TaskResponse:
    """Process satellite imagery task with object detection.
    
    1. Resolve area_id (either provided or snapped from lat/lon)
    2. Fetch imagery (dynamic/static based on mode)
    3. Run SAM detection or load precomputed masks
    4. Compute building stats from detections
    5. Return TaskResponse with BuildingStats and ChangeStats
    
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
        # Static mode: use pre-stored imagery directly
        from pathlib import Path
        path = str(Path(f"data/imagery/{area_id}/{date}.png"))
        if not Path(path).exists():
            # Fallback to fetch if static doesn't exist
            path = fetch_dynamic_imagery(area_id, date)

    width = height = 0
    building_stats = BuildingStats()
    change_stats = ChangeStats()
    
    try:
        img = load_image(path)
        width, height = img.size
        
        # Check for precomputed masks
        mask_dir = Path(f"data/masks/{area_id}")
        mask_path = mask_dir / f"{date}_mask.npy"
        
        detections = []
        if mask_path.exists():
            # Load precomputed mask and extract stats
            mask = np.load(mask_path)
            # Convert mask to simple detections (count connected components)
            from scipy import ndimage
            labeled, num_features = ndimage.label(mask)
            for i in range(1, num_features + 1):
                region = (labeled == i)
                area = np.sum(region)
                if area > 10:  # Filter small noise
                    detections.append({"area": float(area)})
        else:
            # Run SAM detection
            detections = detect_objects(
                path,
                prompt="buildings infrastructure",
                automatic=True,
                min_area=10.0,
            )
        
        # Compute building stats
        aoi = get_aoi(area_id)
        bbox = aoi.get("bbox", [0, 0, 0.01, 0.01])
        # Rough area calculation from bbox (degrees to km)
        # 1 degree latitude  111 km, longitude varies by latitude
        lat_span = abs(bbox[3] - bbox[1])
        lon_span = abs(bbox[2] - bbox[0])
        aoi_area_km2 = lat_span * lon_span * 111 * 111 * 0.8  # crude estimate
        
        building_stats = compute_building_stats(detections, aoi_area_km2)
        
    except Exception as e:
        # If detection fails, return zeros
        print(f"Detection failed: {e}")

    # Placeholder change stats (requires temporal comparison)
    change_stats = ChangeStats()

    results = {
        "area_id": area_id,
        "date": date,
        "mode": mode,
        "pixel_width": width,
        "pixel_height": height,
        "detections_count": building_stats.count,
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
    treq = TaskRequest(lat=lat, lon=lon, date=date, imagery_source="dynamic")
    return loop.run_until_complete(process_task(treq))
