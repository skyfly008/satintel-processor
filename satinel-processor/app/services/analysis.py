import asyncio
from pathlib import Path
from typing import List, Optional
from PIL import Image
import numpy as np

from ..models.schema import TaskRequest, TaskResponse, BatchRequest, BuildingStats, ChangeStats, BatchResponse
from satinel.api_fetch import fetch_dynamic_imagery, fetch_historical_pair
from satinel.imagery_io import load_image, generate_overlay
from satinel.data_config import snap_to_aoi_tile, get_aoi
from satinel.object_model import detect_objects
from satinel.change_detection import compute_change_stats, compute_change_from_masks


def compute_building_stats(detections: List[dict], aoi_area_km2: float = 1.0) -> BuildingStats:
    """Compute building count, total area, and density from detections."""
    if not detections:
        return BuildingStats(count=0, total_footprint_area=0.0, density_per_km2=0.0)
    
    count = len(detections)
    # Convert pixel area to m² (assuming 10m/pixel resolution)
    PIXEL_AREA_M2 = 10 * 10
    total_area_m2 = sum(det.get("area", 0) * PIXEL_AREA_M2 for det in detections)
    density = count / aoi_area_km2 if aoi_area_km2 > 0 else 0.0
    
    return BuildingStats(
        count=count,
        total_footprint_area=total_area_m2,
        density_per_km2=density,
    )


async def process_task(req: TaskRequest) -> TaskResponse:
    """Process imagery with optional temporal comparison.
    
    Single-date mode: detects buildings and computes stats.
    Temporal mode: compares historical and current dates for change detection.
    """
    # Resolve area
    area_id = req.area_id
    if area_id is None and req.lat is not None and req.lon is not None:
        area_id = snap_to_aoi_tile(req.lon, req.lat) or "AREA_1"

    date = req.date or "2023-01-01"
    historical_date = req.historical_date
    mode = req.imagery_source or "static"
    prompt = req.prompt or "buildings infrastructure"

    is_temporal = historical_date is not None
    
    # Helper: get image path for a date
    def get_image_path(target_date: str) -> str:
        if mode == "dynamic":
            return fetch_dynamic_imagery(area_id, target_date, lat=req.lat, lon=req.lon)
        else:
            p = Path(f"data/imagery/{area_id}/{target_date}.png")
            if not p.exists():
                return fetch_dynamic_imagery(area_id, target_date)
            return str(p)
    
    # Helper: get detections for a date
    def get_detections(target_date: str, img_path: str) -> List[dict]:
        mask_dir = Path(f"data/masks/{area_id}")
        mask_path = mask_dir / f"{target_date}_mask.npy"
        
        detections = []
        if mask_path.exists():
            # Load precomputed mask
            mask = np.load(mask_path)
            from scipy import ndimage
            labeled, num_features = ndimage.label(mask)
            
            # Convert connected components to detections with geometry
            for i in range(1, num_features + 1):
                region_mask = (labeled == i)
                area = np.sum(region_mask)
                if area > 10:
                    rows, cols = np.where(region_mask)
                    if len(rows) > 0:
                        from shapely.geometry import box
                        minr, maxr = rows.min(), rows.max()
                        minc, maxc = cols.min(), cols.max()
                        poly = box(minc, minr, maxc, maxr)
                        detections.append({
                            "area": float(area),
                            "geometry": poly,
                            "bbox": [float(minc), float(minr), float(maxc), float(maxr)]
                        })
        else:
            # Run SAM detection
            detections = detect_objects(
                img_path,
                prompt=prompt,
                automatic=True,
                min_area=10.0,
            )
        
        return detections

    width = height = 0
    building_stats = BuildingStats()
    change_stats = ChangeStats()
    
    try:
        if is_temporal:
            path_historical = get_image_path(historical_date)
            path_current = get_image_path(date)
            
            detections_historical = get_detections(historical_date, path_historical)
            detections_current = get_detections(date, path_current)
            
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
            
            # Generate temporal overlay with color-coded changes
            change_polygons = {
                'new': change_dict.get('new_objects', []),
                'removed': change_dict.get('removed_objects', []),
                'unchanged': change_dict.get('matched_objects', [])
            }
            overlay_path = generate_overlay(
                path_current,
                detections_current,
                change_polygons=change_polygons
            )
            
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
            # Single date mode
            path = get_image_path(date)
            img = load_image(path)
            width, height = img.size
            
            detections = get_detections(date, path)
            
            aoi = get_aoi(area_id)
            bbox = aoi.get("bbox", [0, 0, 0.01, 0.01]) if aoi else [0, 0, 0.01, 0.01]
            lat_span = abs(bbox[3] - bbox[1])
            lon_span = abs(bbox[2] - bbox[0])
            aoi_area_km2 = lat_span * lon_span * 111 * 111 * 0.8
            
            building_stats = compute_building_stats(detections, aoi_area_km2)
            
            # Generate single-date overlay (all detections in red)
            overlay_path = generate_overlay(path, detections)
            
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
        print(f"Detection/comparison failed: {e}")
        import traceback
        traceback.print_exc()
        
        overlay_path = None
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
        overlay_url=overlay_path,
        results=results,
    )


async def process_batch(req: BatchRequest) -> BatchResponse:
    """Process multiple tasks in parallel and aggregate results.
    Returns BatchResponse with individual task results and aggregated statistics.
    """
    import time
    import uuid
    
    batch_id = f"batch_{uuid.uuid4().hex[:8]}"
    start_time = time.time()
    
    # Execute all tasks in parallel
    tasks = [process_task(t) for t in req.tasks]
    task_results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Separate successful and failed tasks
    completed_tasks = []
    failed_count = 0
    
    for i, result in enumerate(task_results):
        if isinstance(result, Exception):
            failed_count += 1
            # Create error response
            completed_tasks.append(TaskResponse(
                task_id=f"task_{i}",
                status="error",
                results={"error": str(result)}
            ))
        else:
            completed_tasks.append(result)
    
    # Aggregate statistics
    total_detections = 0
    total_new = 0
    total_removed = 0
    total_area = 0.0
    hotspots = []  # areas with high activity
    
    for task in completed_tasks:
        if task.status == "done" and task.building_stats:
            total_detections += task.building_stats.count
            total_area += task.building_stats.total_footprint_area
            
            if task.change_stats:
                total_new += task.change_stats.new
                total_removed += task.change_stats.removed
                
                # Identify hotspots (high activity score)
                if task.change_stats.activity_score > 70:
                    hotspots.append({
                        "task_id": task.task_id,
                        "activity_score": task.change_stats.activity_score,
                        "area_id": task.results.get("area_id") if task.results else None
                    })
    
    elapsed_time = time.time() - start_time
    
    aggregate_stats = {
        "total_detections": total_detections,
        "total_area_m2": total_area,
        "total_new": total_new,
        "total_removed": total_removed,
        "hotspots": hotspots,
        "processing_time_seconds": round(elapsed_time, 2),
        "avg_detections_per_task": round(total_detections / len(completed_tasks), 1) if completed_tasks else 0
    }
    
    return BatchResponse(
        batch_id=batch_id,
        status="completed",
        total_tasks=len(req.tasks),
        completed=len(completed_tasks) - failed_count,
        failed=failed_count,
        aggregate_stats=aggregate_stats,
        task_results=completed_tasks
    )


def process_task_coords(lat: float, lon: float, date: Optional[str] = None) -> TaskResponse:
    """Synchronous wrapper for shell testing."""
    loop = asyncio.get_event_loop()
    treq = TaskRequest(lat=lat, lon=lon, date=date, imagery_source="dynamic")
    return loop.run_until_complete(process_task(treq))
