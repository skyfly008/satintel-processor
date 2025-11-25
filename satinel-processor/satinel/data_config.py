# Areas of Interest registry
# Format: bbox = [min_lon, min_lat, max_lon, max_lat]
AOI_REGISTRY = {
    "AREA_1": {"name": "Test Airfield", "bbox": [-115.5, 35.5, -114.5, 36.5], "center": (-115.0, 36.0)},
    "AREA_2": {"name": "Test Town", "bbox": [-116.5, 34.5, -115.5, 35.5], "center": (-116.0, 35.0)},
    "AREA_3": {"name": "Reserve", "bbox": [-114.5, 36.5, -113.5, 37.5], "center": (-114.0, 37.0)},
}


def get_aoi(aoi_id: str):
    return AOI_REGISTRY.get(aoi_id)


def snap_to_aoi_tile(lon: float, lat: float, max_degree: float = 1.0) -> str | None:
    """Snap coordinates to nearest AOI within max_degree threshold.
    Returns AOI id if within range, None otherwise.
    """
    for aid, meta in AOI_REGISTRY.items():
        cx, cy = meta.get("center", (0.0, 0.0))
        if abs(cx - lon) <= max_degree and abs(cy - lat) <= max_degree:
            return aid
    return None
