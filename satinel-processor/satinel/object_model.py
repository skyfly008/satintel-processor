# SAM-based object detection for satellite imagery
from typing import List, Dict, Optional
from pathlib import Path
import numpy as np

try:
    from samgeo import SamGeo
except ImportError:
    SamGeo = None

try:
    import rasterio
    from rasterio import features
    from shapely.geometry import shape, Polygon
except ImportError:
    rasterio = None
    features = None
    shape = None
    Polygon = None


# Default model checkpoint paths
DEFAULT_SAM_CHECKPOINT = Path("models/sam_vit_h_4b8939.pth")
FALLBACK_SAM_CHECKPOINT = Path("models/sam_vit_l_0b3195.pth")


def detect_objects(
    image_path: str,
    prompt: str = "buildings infrastructure",
    model_type: str = "vit_h",
    checkpoint: Optional[str] = None,
    return_type: str = "polygons",
    automatic: bool = True,
    min_area: float = 10.0,
) -> List[Dict]:
    """
    Detect objects in satellite imagery using SAM (Segment Anything Model).

    Args:
        image_path: Path to input image (PNG, JPEG, or GeoTIFF)
        prompt: Text description of objects to detect (only used with automatic=False)
        model_type: SAM model variant ('vit_h', 'vit_l', 'vit_b')
        checkpoint: Path to SAM weights file (optional, uses default if None)
        return_type: 'polygons' returns Shapely objects, 'mask' returns binary array
        automatic: Use automatic segmentation (True) or text prompts (False)
        min_area: Minimum polygon area to filter small detections (pixels)

    Returns:
        List of detection dictionaries with 'geometry' (Shapely polygon), 'area', 'bbox'
    """
    if SamGeo is None:
        return []
    
    image_path = Path(image_path)
    
    # Determine checkpoint path
    if checkpoint is None:
        if DEFAULT_SAM_CHECKPOINT.exists():
            checkpoint = str(DEFAULT_SAM_CHECKPOINT)
        elif FALLBACK_SAM_CHECKPOINT.exists():
            checkpoint = str(FALLBACK_SAM_CHECKPOINT)
        else:
            # Let SamGeo auto-download if no local checkpoint
            checkpoint = None

    # Generate output mask path
    output_mask = image_path.parent / f"{image_path.stem}_sam_mask.tif"
    
    try:
        # Initialize SamGeo with adjusted parameters for building detection
        sam_kwargs = {
            "points_per_side": 32,
            "pred_iou_thresh": 0.80,  # Lowered from 0.86 for more detections
            "stability_score_thresh": 0.85,  # Lowered from 0.92 for more detections
            "min_mask_region_area": 25,  # Filter very small regions
        } if automatic else None
        
        sam = SamGeo(
            model_type=model_type,
            checkpoint=checkpoint,
            automatic=automatic,
            sam_kwargs=sam_kwargs
        )

        # Generate masks
        generate_kwargs = {
            "source": str(image_path),
            "output": str(output_mask),
            "foreground": True,
            "batch": True,
        }
        
        if not automatic and prompt:
            generate_kwargs["text_prompt"] = prompt
        
        sam.generate(**generate_kwargs)

        # Load generated mask and convert to polygons
        if not output_mask.exists():
            return []
        
        with rasterio.open(output_mask) as src:
            mask = src.read(1)
            transform = src.transform

        if return_type == "mask":
            output_mask.unlink(missing_ok=True)
            return [{"mask": mask, "transform": transform}]

        # Convert mask to polygons using rasterio shapes
        polygons = []
        for geom, value in features.shapes(mask.astype(np.uint8), transform=transform):
            if value == 1:  # Only foreground objects
                poly = shape(geom)
                
                # Filter by minimum area
                if poly.area < min_area:
                    continue
                
                polygons.append({
                    "geometry": poly,
                    "area": poly.area,
                    "bbox": list(poly.bounds),  # (minx, miny, maxx, maxy)
                    "confidence": 1.0,  # SAM doesn't provide per-object confidence
                })

        # Clean up temporary mask file
        output_mask.unlink(missing_ok=True)

        return polygons

    except Exception as e:
        # Clean up on error
        if output_mask.exists():
            output_mask.unlink(missing_ok=True)
        return []


def precompute_masks(
    image_path: str,
    output_path: str,
    prompt: str = "buildings infrastructure",
    checkpoint: Optional[str] = None,
    automatic: bool = True,
) -> Optional[np.ndarray]:
    """Precompute and save masks for an image.
    
    Args:
        image_path: Path to input image
        output_path: Path to save .npy mask file
        prompt: Detection prompt (for non-automatic mode)
        checkpoint: SAM checkpoint path
        automatic: Use automatic segmentation
    
    Returns:
        Combined mask array or None if detection failed
    """
    detections = detect_objects(
        image_path,
        prompt=prompt,
        checkpoint=checkpoint,
        automatic=automatic,
        return_type="polygons"
    )
    
    if not detections:
        return None
    
    # Load image to get dimensions
    from PIL import Image
    img = Image.open(image_path)
    width, height = img.size
    
    # Create empty mask
    combined_mask = np.zeros((height, width), dtype=np.uint8)
    
    # Rasterize all polygons onto mask
    if features is not None:
        geometries = [(det["geometry"], 1) for det in detections if det.get("geometry")]
        if geometries:
            features.rasterize(
                geometries,
                out=combined_mask,
                fill=0,
                all_touched=True,
            )
    
    # Save mask
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    np.save(output_path, combined_mask)
    return combined_mask