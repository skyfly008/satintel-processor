# AOI registry and snapping logic (stub)
AOI_REGISTRY = {
    "AREA_1": {"bbox": [0,0,1,1], "snap_grid": 0.001},
    "AREA_2": {"bbox": [1,1,2,2], "snap_grid": 0.001}
}


def get_aoi(aoi_id: str):
    return AOI_REGISTRY.get(aoi_id)
