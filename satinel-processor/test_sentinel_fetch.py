"""
Simple sentinelhub connectivity test script.
It reads placeholder credentials from `app.config.settings` and attempts a tiny request.
Replace placeholders in `.env` with real credentials or set environment variables.
"""
from app.config import settings

try:
    from sentinelhub import SHConfig, BBox, CRS, MimeType, SentinelHubRequest, DataCollection, bbox_to_dimensions
except Exception as e:
    print("sentinelhub package is not installed or import failed:", e)
    raise


def main():
    # Build SHConfig using our settings (fields come from .env via pydantic-settings)
    try:
        cfg = SHConfig()
    except Exception:
        cfg = None

    if cfg is not None:
        if getattr(settings, 'sentinel_instance_id', None):
            cfg.instance_id = settings.sentinel_instance_id
        if getattr(settings, 'sentinel_client_id', None):
            cfg.sh_client_id = settings.sentinel_client_id
        if getattr(settings, 'sentinel_client_secret', None):
            cfg.sh_client_secret = settings.sentinel_client_secret

    print('Using instance_id:', cfg.instance_id if cfg is not None else None)

    # quick bbox over a tiny area (example coords)  not tied to AOI registry
    bbox = BBox(bbox=[13.822174, 45.850803, 13.828167, 45.854177], crs=CRS.WGS84)
    size = bbox_to_dimensions(bbox, resolution=10)

    try:
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
        data = request.get_data()
        print('Request completed, received', len(data), 'items')
    except Exception as e:
        print('Sentinel request failed:', e)


if __name__ == '__main__':
    main()
