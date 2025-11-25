from pathlib import Path
from PIL import Image
import numpy as np
from typing import Tuple, Optional

try:
    import rasterio
    from rasterio.io import MemoryFile
except ImportError:
    rasterio = None


def load_image(path: str) -> Image.Image:
    """Load image from path (PNG, JPEG, or GeoTIFF)."""
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
    """Load image as numpy array and optionally load mask.
    
    Returns:
        (image_array, mask_array or None)
    """
    img = load_image(image_path)
    img_arr = np.array(img)
    
    mask_arr = None
    if mask_path and Path(mask_path).exists():
        mask_arr = load_mask(mask_path)
    
    return img_arr, mask_arr


def save_overlay(img: Image.Image, outpath: str):
    """Save overlay image to path (PNG)."""
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
    """Get URL or path for overlay visualization (stub for now)."""
    return image_path
