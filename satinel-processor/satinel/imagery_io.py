from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
from typing import Tuple, Optional, List, Dict

try:
    import rasterio
    from rasterio.io import MemoryFile
except ImportError:
    rasterio = None


def load_image(path: str) -> Image.Image:
    """Load PNG, JPEG, or GeoTIFF image."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)
    
    # Try rasterio first for GeoTIFF support
    if rasterio is not None and p.suffix.lower() in ['.tif', '.tiff']:
        try:
            with rasterio.open(p) as src:
                # Read RGB bands if available
                if src.count >= 3:
                    r = src.read(1)
                    g = src.read(2)
                    b = src.read(3)
                    arr = np.dstack([r, g, b])
                else:
                    arr = src.read(1)
                return Image.fromarray(arr.astype('uint8'))
        except Exception:
            pass
    
    return Image.open(p)


def load_image_and_mask(image_path: str, mask_path: Optional[str] = None) -> Tuple[np.ndarray, Optional[np.ndarray]]:
    """Load image and optional mask as numpy arrays."""
    img = load_image(image_path)
    img_arr = np.array(img)
    
    mask_arr = None
    if mask_path and Path(mask_path).exists():
        mask_arr = load_mask(mask_path)
    
    return img_arr, mask_arr


def save_overlay(img: Image.Image, outpath: str):
    """Save overlay image as PNG."""
    p = Path(outpath)
    p.parent.mkdir(parents=True, exist_ok=True)
    img.save(p)


def save_tiff(array: np.ndarray, outpath: str, crs: str = 'EPSG:4326', transform=None):
    """Save numpy array as GeoTIFF."""
    if rasterio is None:
        raise ImportError("rasterio required for GeoTIFF save")
    
    p = Path(outpath)
    p.parent.mkdir(parents=True, exist_ok=True)
    
    if array.ndim == 2:
        count = 1
        height, width = array.shape
    else:
        height, width, count = array.shape
    
    with rasterio.open(
        p, 'w',
        driver='GTiff',
        height=height,
        width=width,
        count=count,
        dtype=array.dtype,
        crs=crs,
        transform=transform,
    ) as dst:
        if count == 1:
            dst.write(array, 1)
        else:
            for i in range(count):
                dst.write(array[:, :, i], i + 1)


def load_mask(path: str) -> np.ndarray:
    """Load mask from .npy file."""
    return np.load(path)


def get_overlay_url(image_path: str) -> str:
    """Get path for overlay visualization."""
    return image_path


def generate_overlay(
    image_path: str,
    detections: List[dict],
    change_polygons: Optional[Dict[str, List[dict]]] = None,
    output_path: Optional[str] = None
) -> str:
    """Generate overlay visualization with detected objects and changes.
    
    Single-date mode: draws yellow semi-transparent polygons for all detections.
    Temporal mode: draws green for new objects, red for removed, yellow for unchanged.
    
    Color scheme:
    - Yellow (255,255,0): All buildings/infrastructure in single-date mode or unchanged
    - Green (0,255,0): New buildings detected (added since historical)
    - Red (255,0,0): Removed buildings (present in historical, gone in current)
    
    Returns path to saved overlay PNG.
    """
    img = load_image(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Create overlay layer with transparency
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, 'RGBA')
    
    if change_polygons is None:
        # Single-date mode: draw all detections in yellow
        for det in detections:
            _draw_polygon(draw, det, color=(255, 255, 0, 128))  # Yellow, 50% opacity
    else:
        # Temporal mode: color-code by change type
        # Draw in order: unchanged (yellow) first, then new (green), then removed (red) on top
        
        # 1. Yellow for unchanged buildings (base layer)
        unchanged = change_polygons.get('unchanged', [])
        for det in unchanged:
            _draw_polygon(draw, det, color=(255, 255, 0, 100))  # Yellow, more transparent
        
        # 2. Green for new buildings (highlight growth)
        new = change_polygons.get('new', [])
        for det in new:
            _draw_polygon(draw, det, color=(0, 255, 0, 150))  # Bright green, more opaque
        
        # 3. Red for removed buildings (highlight demolition/change)
        removed = change_polygons.get('removed', [])
        for det in removed:
            _draw_polygon(draw, det, color=(255, 0, 0, 150))  # Bright red, more opaque
    
    # Composite overlay onto base image
    img_rgba = img.convert('RGBA')
    result = Image.alpha_composite(img_rgba, overlay)
    result = result.convert('RGB')
    
    # Save overlay
    if output_path is None:
        # Auto-generate path from image path
        p = Path(image_path)
        area_id = p.parent.name
        date_str = p.stem
        output_path = f"data/overlays/{area_id}/{date_str}_overlay.png"
    
    save_overlay(result, output_path)
    return output_path


def _draw_polygon(draw: ImageDraw.ImageDraw, detection: dict, color: tuple):
    """Helper to draw a single polygon from detection dict.
    
    Args:
        draw: PIL ImageDraw object
        detection: Detection dict with 'geometry' or 'bbox'
        color: RGBA tuple (R, G, B, Alpha) for fill color
    """
    from shapely.geometry import Polygon
    
    geometry = detection.get('geometry')
    if geometry is None:
        # Fall back to bbox if no geometry
        bbox = detection.get('bbox')
        if bbox:
            minc, minr, maxc, maxr = bbox
            coords = [(minc, minr), (maxc, minr), (maxc, maxr), (minc, maxr)]
            # Draw with solid outline
            outline_color = (color[0], color[1], color[2], 255)
            draw.polygon(coords, fill=color, outline=outline_color, width=2)
        return
    
    # Handle Shapely geometry
    if hasattr(geometry, 'exterior'):
        coords = list(geometry.exterior.coords)
        # Convert to pixel coordinates (already in pixel space)
        pixel_coords = [(x, y) for x, y in coords]
        if len(pixel_coords) >= 3:
            # Draw with slightly more visible outline
            outline_color = (color[0], color[1], color[2], 255)
            draw.polygon(pixel_coords, fill=color, outline=outline_color, width=2)

