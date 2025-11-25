import asyncio
from pathlib import Path
from typing import List, Optional
from PIL import Image
import numpy as np

from ..models.schema import TaskRequest, TaskResponse, BatchRequest, BuildingStats, ChangeStats
from satinel.api_fetch import fetch_dynamic_imagery, fetch_historical_pair
from satinel.imagery_io import load_image
from satinel.data_config import snap_to_aoi_tile, get_aoi
from satinel.object_model import detect_objects
from satinel.change_detection import compute_change_stats, compute_change_from_masks


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
    """Process satellite imagery task with object detection and optional temporal comparison.
    
    Workflow:
    1. Resolve area_id (either provided or snapped from lat/lon)
    2. Fetch imagery (single or pair if historical_date provided)
    3. Run SAM detection or load precomputed masks
    4. If historical_date: compute change statistics
    5. Return TaskResponse with BuildingStats and ChangeStats
    
    Args:
        req: TaskRequest with optional historical_date for temporal comparison
    
    Returns:
        TaskResponse with detection results and change statistics
    """
    # Resolve area
    area_id = req.area_id
    if area_id is None and req.lat is not None and req.lon is not None:
        area_id = snap_to_aoi_tile(req.lon, req.lat) or "AREA_1"  # default fallback

    date = req.date or "2023-01-01"
    historical_date = req.historical_date
    mode = req.imagery_source or "static"

    # Determine if we need temporal comparison
    is_temporal = historical_date is not None
    
    # Helper function to get image path
    def get_image_path(target_date: str) -> str:
        if mode == "dynamic":
            return fetch_dynamic_imagery(area_id, target_date, lat=req.lat, lon=req.lon)
        else:
            # Static mode: use pre-stored imagery directly
            p = Path(f"data/imagery/{area_id}/{target_date}.png")
            if not p.exists():
                # Fallback to fetch if static doesn't exist
                return fetch_dynamic_imagery(area_id, target_date)
            return str(p)
    
    # Helper function to get detections for a date
    def get_detections(target_date: str, img_path: str) -> List[dict]:
        mask_dir = Path(f"data/masks/{area_id}")
        mask_path = mask_dir / f"{target_date}_mask.npy"
        
        detections = []
        if mask_path.exists():
            # Load precomputed mask and extract detections with geometry
            mask = np.load(mask_path)
            from scipy import ndimage
            labeled, num_features = ndimage.label(mask)
            
            # Convert connected components to detections
            for i in range(1, num_features + 1):
                region_mask = (labeled == i)
                area = np.sum(region_mask)
                if area > 10:  # Filter small noise
                    # Create simple bounding box geometry
                    rows, cols = np.where(region_mask)
                    if len(rows) > 0:
                        from shapely.geometry import box
                        minr, maxr = rows.min(), rows.max()
                        minc, maxc = cols.min(), cols.max()
                        # Create polygon from bbox
                        poly = box(minc, minr, maxc, maxr)
                        detections.append({
                            "area": float(area),
                            "geometry": poly,
                            "bbox": [float(minc), float(minr), float(maxc), float(maxr)]
                        })
        else:
            # Run SAM detection (returns polygons with geometry)
            detections = detect_objects(
                img_path,
                prompt="buildings infrastructure",
                automatic=True,
                min_area=10.0,
            )
        
        return detections

    width = height = 0
    building_stats = BuildingStats()
    change_stats = ChangeStats()
    
    try:
        if is_temporal:
            # Temporal comparison mode
            path_historical = get_image_path(historical_date)
            path_current = get_image_path(date)
            
            # Get detections for both dates
            detections_historical = get_detections(historical_date, path_historical)
            detections_current = get_detections(date, path_current)
            
            # Load current image for dimensions
            img = load_image(path_current)
            width, height = img.size
            
            # Compute change statistics
            change_dict = compute_change_stats(detections_historical, detections_current)
            change_stats = ChangeStats(**change_dict)
            
            # Compute building stats for current date
            aoi = get_aoi(area_id)
            bbox = aoi.get("bbox", [0, 0, 0.01, 0.01]) if aoi else [0, 0, 0.01, 0.01]
            lat_span = abs(bbox[3] - bbox[1])
            lon_span = abs(bbox[2] - bbox[0])
            aoi_area_km2 = lat_span * lon_span * 111 * 111 * 0.8
            
            building_stats = compute_building_stats(detections_current, aoi_area_km2)
            
            results = {
                "area_id": area_id,
                "date": date,
                "historical_date": historical_date,
                "mode": mode,
                "pixel_width": width,
                "pixel_height": height,
                "detections_current": len(detections_current),
                "detections_historical": len(detections_historical),
                "imagery_path_current": path_current,
                "imagery_path_historical": path_historical,
            }
        else:
            # Single date mode (original behavior)
            path = get_image_path(date)
            img = load_image(path)
            width, height = img.size
            
            detections = get_detections(date, path)
            
            # Compute building stats
            aoi = get_aoi(area_id)
            bbox = aoi.get("bbox", [0, 0, 0.01, 0.01]) if aoi else [0, 0, 0.01, 0.01]
            lat_span = abs(bbox[3] - bbox[1])
            lon_span = abs(bbox[2] - bbox[0])
            aoi_area_km2 = lat_span * lon_span * 111 * 111 * 0.8
            
            building_stats = compute_building_stats(detections, aoi_area_km2)
            
            results = {
                "area_id": area_id,
                "date": date,
                "mode": mode,
                "pixel_width": width,
                "pixel_height": height,
                "detections_count": building_stats.count,
                "imagery_path": path,
            }
        
    except Exception as e:
        # If detection fails, return zeros
        print(f"Detection/comparison failed: {e}")
        import traceback
        traceback.print_exc()
        
        results = {
            "area_id": area_id,
            "date": date,
            "error": str(e)
        }

    task_id = req.task_id or f"{area_id}:{date}"
    if is_temporal:
        task_id = f"{area_id}:{historical_date}-{date}"
    
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
