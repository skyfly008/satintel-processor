from typing import List
from app.config import settings

try:
    from sentinelhub import SHConfig, BBox, CRS, MimeType, SentinelHubRequest, DataCollection, bbox_to_dimensions
except Exception:
    SHConfig = None
    SentinelHubRequest = None

try:
    import usgs
except Exception:
    usgs = None

from satinel.data_config import get_aoi
from pathlib import Path
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


def _save_remote_to(path: Path, url: str):
    # simple downloader
    resp = requests.get(url, stream=True, timeout=60)
    resp.raise_for_status()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    return path


def fetch_dynamic_imagery(area_id: str, date: str) -> str:
    """Try Sentinel Hub first, then USGS as a fallback. Otherwise return local static path.

    This function attempts to fetch a tile for (area_id, date). It will:
    - Try to use Sentinel Hub if available and credentials present.
    - If that fails and USGS is available and `settings.usgs_api_key` is set, try USGS.
    - On success save to `data/cache/` and return the path.
    - If network fetches are not possible, return the pre-stored static path.
    """
    static_path = Path(f"data/imagery/{area_id}/{date}.png")

    # 1) Attempt Sentinel Hub (if we have the client)
    data_obtained = False
    if SentinelHubRequest is not None:
        try:
            cfg = _build_sh_config()
            if cfg is not None:
                # Build a quick bbox from AOI if available
                aoi = get_aoi(area_id)
                if aoi is not None:
                    b = aoi.get('bbox')
                    bbox = BBox(bbox=b, crs=CRS.WGS84)
                    size = bbox_to_dimensions(bbox, resolution=10)
                    request = SentinelHubRequest(
                        evalscript="""
                            //VERSION=3
                            function setup(){return {input:[{band:\"B04\"},{band:\"B03\"},{band:\"B02\"}],output:{bands:3}}}
                            function evaluatePixel(sample){return [sample.B04,sample.B03,sample.B02]}
                        """,
                        input_data=[SentinelHubRequest.input_data(DataCollection.SENTINEL2_L2A)],
                        responses=[SentinelHubRequest.output_response('default', MimeType.PNG)],
                        bbox=bbox,
                        size=size,
                        config=cfg,
                    )
                    res = request.get_data()
                    if res:
                        # write first item to cache
                        out = CACHE_DIR / f"{area_id}_{date}_sentinel.png"
                        with open(out, 'wb') as f:
                            f.write(res[0])
                        return str(out)
        except Exception:
            # Sentinel failed; continue to USGS fallback
            pass

    # 2) USGS fallback
    if usgs is not None and settings.usgs_api_key:
        try:
            # login once per process
            try:
                usgs.login(settings.usgs_api_key)
            except Exception:
                # some usgs libs use different auth methods; ignore login error
                pass

            aoi = get_aoi(area_id)
            if aoi is not None:
                # Use bbox and date to search
                b = aoi.get('bbox')
                # usgs.search API may vary; we attempt a common pattern
                begin = date
                end = date
                try:
                    results = usgs.search('LANDSAT_8_C2', 'EE', bbox=b, begin=begin, end=end)
                except Exception:
                    results = None

                if results and isinstance(results, dict) and results.get('data'):
                    scene = results['data'][0]
                    scene_id = scene.get('entityId') or scene.get('displayId')
                    if scene_id:
                        try:
                            dl = usgs.download('LANDSAT_8_C2', 'EE', [scene_id], product='SR')
                            # dl may be a dict or list with URLs; attempt to find a URL
                            url = None
                            if isinstance(dl, dict):
                                # try common keys
                                url = dl.get('data', {}).get('url') or dl.get('url')
                            elif isinstance(dl, list) and dl:
                                url = dl[0]
                            if url:
                                out = CACHE_DIR / f"{area_id}_{date}_usgs.png"
                                _save_remote_to(out, url)
                                return str(out)
                        except Exception:
                            pass
        except Exception:
            pass

    # 3) fallback to static pre-stored imagery
    if static_path.exists():
        return str(static_path)

    # 4) nothing found  return static path (caller should handle missing file)
    return str(static_path)


def batch_fetch(tasks: List[dict]) -> List[str]:
    return [fetch_dynamic_imagery(t['area_id'], t['date']) for t in tasks]
