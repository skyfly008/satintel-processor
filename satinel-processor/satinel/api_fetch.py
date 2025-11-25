from typing import List, Optional
from app.config import settings

try:
    from sentinelhub import SHConfig, BBox, CRS, MimeType, SentinelHubRequest, DataCollection
except Exception:
    SHConfig = None
    SentinelHubRequest = None
    BBox = None
    CRS = None

try:
    import usgs
except Exception:
    usgs = None

from satinel.data_config import get_aoi
from pathlib import Path
from PIL import Image
import requests

CACHE_DIR = Path('data/cache')
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _build_sh_config():
    if SHConfig is None:
        return None
    config = SHConfig()
    config.instance_id = settings.sentinel_instance_id
    config.sh_client_id = settings.sentinel_client_id
    config.sh_client_secret = settings.sentinel_client_secret
    config.sh_base_url = "https://services.sentinel-hub.com"
    return config


def _bbox_around_point(lon: float, lat: float, size_deg: float = 0.01) -> list:
    """Create a bbox [min_lon, min_lat, max_lon, max_lat] around a point (~1km at equator)."""
    half = size_deg / 2
    return [lon - half, lat - half, lon + half, lat + half]


def _save_remote_to(path: Path, url: str):
    """Download from URL and save to path."""
    resp = requests.get(url, stream=True, timeout=60)
    resp.raise_for_status()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    return path


def fetch_dynamic_imagery(area_id: str, date: str, lat: Optional[float] = None, lon: Optional[float] = None) -> str:
    """Fetch imagery dynamically (Sentinel Hub -> USGS -> static fallback).
    
    If lat/lon provided, fetch 512x512 clip around that point.
    Otherwise use AOI bbox.
    
    Returns path to cached PNG.
    """
    static_path = Path(f"data/imagery/{area_id}/{date}.png")

    # Determine bbox
    bbox_coords = None
    if lat is not None and lon is not None:
        bbox_coords = _bbox_around_point(lon, lat, size_deg=0.01)
    else:
        aoi = get_aoi(area_id)
        if aoi:
            bbox_coords = aoi.get('bbox')

    # 1) Attempt Sentinel Hub
    if SentinelHubRequest is not None and bbox_coords:
        try:
            cfg = _build_sh_config()
            if cfg is not None and cfg.instance_id:
                bbox = BBox(bbox=bbox_coords, crs=CRS.WGS84)
                size = (512, 512)
                
                request = SentinelHubRequest(
                    evalscript="""
                        //VERSION=3
                        function setup(){return {input:[{bands:["B04","B03","B02"]}],output:{bands:3,sampleType:"UINT8"}}}
                        function evaluatePixel(sample){return [sample.B04*255,sample.B03*255,sample.B02*255]}
                    """,
                    input_data=[SentinelHubRequest.input_data(
                        DataCollection.SENTINEL2_L2A,
                        time_interval=(date, date)
                    )],
                    responses=[SentinelHubRequest.output_response('default', MimeType.PNG)],
                    bbox=bbox,
                    size=size,
                    config=cfg,
                )
                res = request.get_data()
                if res and len(res) > 0:
                    cache_name = f"{area_id}_{date}_sentinel_{lon}_{lat}.png" if lat and lon else f"{area_id}_{date}_sentinel.png"
                    out = CACHE_DIR / cache_name
                    with open(out, 'wb') as f:
                        f.write(res[0])
                    return str(out)
        except Exception:
            pass

    # 2) USGS fallback
    if usgs is not None and settings.usgs_api_key and bbox_coords:
        try:
            try:
                usgs.login(settings.usgs_api_key)
            except Exception:
                pass

            begin = date
            end = date
            try:
                results = usgs.search('LANDSAT_8_C2', 'EE', bbox=bbox_coords, begin=begin, end=end)
            except Exception:
                results = None

            if results and isinstance(results, dict) and results.get('data'):
                scene = results['data'][0]
                scene_id = scene.get('entityId') or scene.get('displayId')
                if scene_id:
                    try:
                        dl = usgs.download('LANDSAT_8_C2', 'EE', [scene_id], product='SR')
                        url = None
                        if isinstance(dl, dict):
                            url = dl.get('data', {}).get('url') or dl.get('url')
                        elif isinstance(dl, list) and dl:
                            url = dl[0]
                        if url:
                            cache_name = f"{area_id}_{date}_usgs_{lon}_{lat}.tif" if lat and lon else f"{area_id}_{date}_usgs.tif"
                            out_tif = CACHE_DIR / cache_name
                            _save_remote_to(out_tif, url)
                            out_png = out_tif.with_suffix('.png')
                            try:
                                img = Image.open(out_tif)
                                img = img.resize((512, 512), Image.LANCZOS)
                                img.save(out_png)
                                return str(out_png)
                            except Exception:
                                return str(out_tif)
                    except Exception:
                        pass
        except Exception:
            pass

    # 3) Fallback to static
    if static_path.exists():
        return str(static_path)

    return str(static_path)


def batch_fetch(tasks: List[dict]) -> List[str]:
    """Batch fetch with optional lat/lon per task."""
    return [fetch_dynamic_imagery(
        t.get('area_id', 'AREA_1'),
        t.get('date', '2023-01-01'),
        t.get('lat'),
        t.get('lon')
    ) for t in tasks]


def fetch_historical_pair(
    area_id: str,
    date_current: str,
    date_historical: str,
    lat: Optional[float] = None,
    lon: Optional[float] = None
) -> tuple[str, str]:
    """Fetch a pair of images for temporal comparison.
    
    Args:
        area_id: Area identifier
        date_current: Current/target date (e.g., "2023-01-01")
        date_historical: Historical date for comparison (e.g., "2021-01-01")
        lat: Optional latitude for point-based fetching
        lon: Optional longitude for point-based fetching
    
    Returns:
        Tuple of (historical_path, current_path)
    """
    path_historical = fetch_dynamic_imagery(area_id, date_historical, lat, lon)
    path_current = fetch_dynamic_imagery(area_id, date_current, lat, lon)
    
    return path_historical, path_current

