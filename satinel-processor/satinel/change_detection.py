"""Temporal change detection for satellite imagery analysis."""
from typing import Dict, List, Tuple
import numpy as np
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
from scipy import ndimage


def compute_change_stats(
    detections_before: List[Dict],
    detections_after: List[Dict],
    iou_threshold: float = 0.3
) -> Dict:
    """Compare detections between two dates using IoU matching.
    
    Matches objects between dates based on geometric overlap (IoU).
    Computes new, removed, and unchanged object counts plus activity metrics.
    """
    if not detections_before and not detections_after:
        return {
            "new": 0,
            "removed": 0,
            "unchanged": 0,
            "activity_score": 0.0,
            "temporal_change_pct": 0.0,
        }
    
    # Extract polygons
    polys_before = [d["geometry"] for d in detections_before if d.get("geometry")]
    polys_after = [d["geometry"] for d in detections_after if d.get("geometry")]
    
    if not polys_before and not polys_after:
        return {
            "new": 0,
            "removed": 0,
            "unchanged": 0,
            "activity_score": 0.0,
            "temporal_change_pct": 0.0,
        }
    
    # Match objects between dates using IoU
    matched_before = set()
    matched_after = set()
    
    for i, poly_before in enumerate(polys_before):
        best_iou = 0.0
        best_match = -1
        
        for j, poly_after in enumerate(polys_after):
            if j in matched_after:
                continue
            
            try:
                # Compute IoU (Intersection over Union)
                intersection = poly_before.intersection(poly_after).area
                union = poly_before.union(poly_after).area
                
                if union > 0:
                    iou = intersection / union
                    if iou > best_iou and iou >= iou_threshold:
                        best_iou = iou
                        best_match = j
            except Exception:
                continue
        
        if best_match >= 0:
            matched_before.add(i)
            matched_after.add(best_match)
    
    # Compute statistics
    unchanged = len(matched_before)
    removed = len(polys_before) - unchanged
    new = len(polys_after) - unchanged
    
    # Compute activity score (0-100)
    total_before = len(polys_before)
    total_after = len(polys_after)
    max_count = max(total_before, total_after)
    
    if max_count > 0:
        change_ratio = (new + removed) / max_count
        activity_score = min(100.0, change_ratio * 100)
    else:
        activity_score = 0.0
    
    # Compute percentage change
    if total_before > 0:
        temporal_change_pct = ((total_after - total_before) / total_before) * 100
    elif total_after > 0:
        temporal_change_pct = 100.0  # All new
    else:
        temporal_change_pct = 0.0
    
    return {
        "new": new,
        "removed": removed,
        "unchanged": unchanged,
        "activity_score": round(activity_score, 2),
        "temporal_change_pct": round(temporal_change_pct, 2),
    }


def compute_mask_diff(mask_before: np.ndarray, mask_after: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Pixel-level diff between two binary masks.
    Returns (new_mask, removed_mask, unchanged_mask).
    """
    # Ensure binary masks
    mask_before = (mask_before > 0).astype(np.uint8)
    mask_after = (mask_after > 0).astype(np.uint8)
    
    # Compute differences
    new_mask = np.logical_and(mask_after == 1, mask_before == 0).astype(np.uint8)
    removed_mask = np.logical_and(mask_before == 1, mask_after == 0).astype(np.uint8)
    unchanged_mask = np.logical_and(mask_before == 1, mask_after == 1).astype(np.uint8)
    
    return new_mask, removed_mask, unchanged_mask


def compute_change_from_masks(
    mask_before: np.ndarray,
    mask_after: np.ndarray,
    min_object_size: int = 10
) -> Dict:
    """Compute change stats from masks using connected components."""
    new_mask, removed_mask, unchanged_mask = compute_mask_diff(mask_before, mask_after)
    
    # Count objects using connected components
    labeled_new, num_new = ndimage.label(new_mask)
    labeled_removed, num_removed = ndimage.label(removed_mask)
    labeled_unchanged, num_unchanged = ndimage.label(unchanged_mask)
    
    # Filter small objects
    for labeled, num in [(labeled_new, num_new), (labeled_removed, num_removed), (labeled_unchanged, num_unchanged)]:
        for i in range(1, num + 1):
            if np.sum(labeled == i) < min_object_size:
                if labeled is labeled_new:
                    num_new -= 1
                elif labeled is labeled_removed:
                    num_removed -= 1
                else:
                    num_unchanged -= 1
    
    # Compute metrics
    total_before = num_unchanged + num_removed
    total_after = num_unchanged + num_new
    max_count = max(total_before, total_after)
    
    if max_count > 0:
        change_ratio = (num_new + num_removed) / max_count
        activity_score = min(100.0, change_ratio * 100)
    else:
        activity_score = 0.0
    
    if total_before > 0:
        temporal_change_pct = ((total_after - total_before) / total_before) * 100
    elif total_after > 0:
        temporal_change_pct = 100.0
    else:
        temporal_change_pct = 0.0
    
    return {
        "new": num_new,
        "removed": num_removed,
        "unchanged": num_unchanged,
        "activity_score": round(activity_score, 2),
        "temporal_change_pct": round(temporal_change_pct, 2),
    }
