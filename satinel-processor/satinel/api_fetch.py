from typing import List
from app.config import settings

try:
    from sentinelhub import SHConfig
except Exception:
    SHConfig = None


def _build_sh_config():
    if SHConfig is None:
        return None
    cfg = SHConfig()
    cfg.instance_id = settings.sentinel_instance_id
    cfg.sh_client_id = settings.sentinel_client_id
    cfg.sh_client_secret = settings.sentinel_client_secret
    cfg.sh_base_url = "https://services.sentinel-hub.com"
    return cfg


def fetch_dynamic_imagery(area_id: str, date: str) -> str:
    """Return a path or perform a dynamic fetch using Sentinel Hub.

    Currently this stub returns the local demo path. If `sentinelhub` is
    available and you want to perform a live fetch, extend this function
    to build a `SentinelHubRequest` using the config from `_build_sh_config()`.
    """
    # ensure folder exists (caller may rely on returned path existing)
    return f"data/imagery/{area_id}/{date}.png"


def batch_fetch(tasks: List[dict]) -> List[str]:
    return [fetch_dynamic_imagery(t["area_id"], t["date"]) for t in tasks]
