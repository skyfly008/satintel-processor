"""
Simple sentinelhub connectivity test script.
It reads placeholder credentials from `app.config.settings` and attempts a tiny request.
Replace placeholders in `.env` with real credentials or set environment variables.
"""
from satinel.api_fetch import fetch_dynamic_imagery
from pathlib import Path


def main():
    # Try to fetch for AREA_1 on 2023-01-01 — will use Sentinel then USGS fallback, or static file
    out = fetch_dynamic_imagery('AREA_1', '2023-01-01')
    print('fetch_dynamic_imagery returned:', out)
    path = Path(out)
    if path.exists():
        print('File exists:', path)
    else:
        print('File does not exist; check .env credentials or local data/imagery/AREA_1')


if __name__ == '__main__':
    main()
