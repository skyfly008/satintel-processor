# Data Acquisition Guide

This guide explains how to predownload satellite imagery for the ASIP project.

## Overview

The data acquisition script downloads high-resolution satellite imagery from Sentinel-2 for six predefined Areas of Interest (AOIs):

### New York AOIs:
1. **Manhattan Urban Core** (40.70-40.85°N, 74.02-73.92°W) - Dense urban buildings
2. **JFK Airport** (40.62-40.66°N, 73.82-73.76°W) - Airport infrastructure  
3. **Industrial Brooklyn** (40.65-40.70°N, 73.95-73.90°W) - Warehouses and factories

### Tehran AOIs:
1. **Central Urban** (35.68-35.75°N, 51.35-51.45°E) - Dense residential/commercial
2. **Tehran Airport** (35.40-35.45°N, 51.10-51.20°E) - Airfield infrastructure
3. **Industrial Outskirts** (35.65-35.70°N, 51.25-51.35°E) - Factories and expansion

## Prerequisites

### 1. Install Required Packages

```bash
pip install sentinelhub Pillow
```

Optional (for Landsat fallback):
```bash
pip install landsatxplore rasterio
```

### 2. Verify API Credentials

Ensure your `.env` file has the Sentinel Hub credentials:
```
SENTINEL_INSTANCE_ID=your-instance-id
SENTINEL_CLIENT_ID=your-client-id
SENTINEL_CLIENT_SECRET=your-client-secret
```

Get credentials at: https://www.sentinel-hub.com/

## Running the Script

### Basic Usage

```bash
cd c:\Users\ML05\Projects\ASIP\satinel-processor
python scripts\download_imagery.py
```

### What It Does

1. **Creates directory structure:**
   ```
   data/imagery/
   ├── nyc_manhattan/
   ├── nyc_jfk/
   ├── nyc_industrial/
   ├── tehran_central/
   ├── tehran_airport/
   └── tehran_industrial/
   ```

2. **Downloads imagery** for each AOI with:
   - Date ranges: January 2023 and June 2023
   - Resolution: 10m per pixel (Sentinel-2)
   - Image size: 512x512 pixels
   - Cloud cover: <10%

3. **Saves metadata** to `data/metadata/imagery_metadata.json`

## Output Structure

Each AOI folder will contain PNG files named by date:
```
data/imagery/nyc_manhattan/
├── 2023-01-01.png
└── 2023-06-01.png
```

Metadata file includes:
- AOI name and bounding box
- Date range
- File path
- Source (Sentinel-2)
- Resolution (10m)
- Download timestamp

## Expected Results

- **Images per AOI:** 2 (one per date range)
- **Total images:** ~12 (6 AOIs × 2 dates)
- **Total size:** <100 MB
- **Format:** PNG (512×512, RGB)

## Troubleshooting

### API Rate Limits
- Sentinel Hub free tier: 2,500 requests/month
- If rate-limited, wait or upgrade plan

### No Cloud-Free Images
- Script may skip dates with >10% cloud cover
- Try adjusting `MAX_CLOUD_COVER` in the script
- Or change `DATE_RANGES` to different seasons

### Authentication Errors
- Verify credentials in `.env` file
- Check Sentinel Hub dashboard for account status
- Ensure client ID and secret are correct

### Import Errors
```bash
# If sentinelhub missing:
pip install sentinelhub

# If PIL missing:
pip install Pillow
```

## Customization

### Add New AOIs

Edit `AOIS` dictionary in `scripts/download_imagery.py`:
```python
'my_aoi': {
    'name': 'My Custom Area',
    'bbox': [lon_min, lat_min, lon_max, lat_max],
    'description': 'Description here',
    'mgrs': 'GRID_CODE'
}
```

### Change Date Ranges

Edit `DATE_RANGES` list:
```python
DATE_RANGES = [
    ('2022-01-01', '2022-01-31'),
    ('2024-01-01', '2024-01-31')
]
```

### Adjust Image Size

Change `IMAGE_SIZE`:
```python
IMAGE_SIZE = [1024, 1024]  # Larger images
```

## Data Usage in ASIP

Downloaded imagery is used by:
1. **Building Detection:** ML models identify structures
2. **Object Detection:** Runways, parking lots, etc.
3. **Live Fallback:** If user requests non-cached area, app fetches on-demand

## Next Steps

After downloading imagery:
1. ✓ Run the script to download images
2. → Verify images in `data/imagery/` folders
3. → Check metadata in `data/metadata/`
4. → Run building detection preprocessing (separate script)
5. → Start the ASIP web application

## Additional Resources

- Sentinel Hub API Docs: https://docs.sentinel-hub.com/
- Sentinel-2 Bands Reference: https://sentinel.esa.int/web/sentinel/user-guides/sentinel-2-msi
- USGS EarthExplorer: https://earthexplorer.usgs.gov/
