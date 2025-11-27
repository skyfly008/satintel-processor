# Data Acquisition Setup - Complete ✓

## What Was Created

### 1. Core Scripts

#### `scripts/download_imagery.py`
Main script to download satellite imagery from Sentinel-2 API.
- Downloads 6 AOIs (New York & Tehran)
- 2 date ranges per AOI (Jan & Jun 2023)
- 10m resolution, 512×512 pixel images
- Saves metadata to JSON file

#### `scripts/test_api.py`
Test Sentinel Hub API connection before downloading.
- Verifies credentials in .env
- Tests API connectivity
- Retrieves small test image

#### `scripts/setup_dirs.py`
Creates required directory structure for data storage.

---

### 2. Batch Files (Windows)

#### `scripts/setup_complete.bat`
**One-click complete setup** - runs all steps:
1. Install dependencies
2. Create directories
3. Test API
4. Download imagery

#### `scripts/run_download.bat`
Run only the download step.

#### `scripts/test_api.bat`
Run only the API test.

---

### 3. Documentation

#### `QUICKSTART_DOWNLOAD.md`
Step-by-step guide with troubleshooting.

#### `scripts/DATA_ACQUISITION.md`
Detailed documentation on:
- AOI definitions
- API usage
- Customization
- Troubleshooting

#### `scripts/README.md`
Overview of all scripts and usage.

---

### 4. Configuration Updates

#### `.env` (Your existing file - updated)
Added fields for:
- `USGS_USERNAME` (optional)
- `USGS_PASSWORD` (optional)

#### `.env.example` (Updated)
Added:
- `SENTINEL_INSTANCE_ID`
- `USGS_USERNAME`
- `USGS_PASSWORD`

#### `requirements.txt` (Updated)
Added packages:
- `sentinelhub==3.9.0`
- `landsatxplore==0.14.0`
- `rasterio==1.3.9`

---

## Areas of Interest (AOIs)

### New York (3 AOIs)
1. **Manhattan Urban Core**
   - Coordinates: 40.70-40.85°N, 74.02-73.92°W
   - Purpose: Dense urban buildings detection
   
2. **JFK Airport**
   - Coordinates: 40.62-40.66°N, 73.82-73.76°W
   - Purpose: Airport infrastructure detection

3. **Industrial Brooklyn**
   - Coordinates: 40.65-40.70°N, 73.95-73.90°W
   - Purpose: Warehouses and factories

### Tehran (3 AOIs)
1. **Central Urban**
   - Coordinates: 35.68-35.75°N, 51.35-51.45°E
   - Purpose: Dense residential/commercial

2. **Tehran International Airport**
   - Coordinates: 35.40-35.45°N, 51.10-51.20°E
   - Purpose: Airfield infrastructure

3. **Industrial Outskirts**
   - Coordinates: 35.65-35.70°N, 51.25-51.35°E
   - Purpose: Factories and expansion areas

---

## Directory Structure

```
satinel-processor/
├── scripts/
│   ├── download_imagery.py          ← Main download script
│   ├── test_api.py                  ← API connection test
│   ├── setup_dirs.py                ← Directory setup
│   ├── setup_complete.bat           ← One-click setup (Windows)
│   ├── run_download.bat             ← Download only
│   ├── test_api.bat                 ← Test only
│   ├── DATA_ACQUISITION.md          ← Detailed docs
│   └── README.md                    ← Scripts overview
│
├── data/
│   ├── imagery/                     ← Downloaded images go here
│   │   ├── nyc_manhattan/
│   │   ├── nyc_jfk/
│   │   ├── nyc_industrial/
│   │   ├── tehran_central/
│   │   ├── tehran_airport/
│   │   └── tehran_industrial/
│   ├── masks/                       ← For future preprocessing
│   ├── cache/                       ← For live API caching
│   └── metadata/                    ← imagery_metadata.json
│
├── .env                             ← Your API keys (updated)
├── .env.example                     ← Template (updated)
├── requirements.txt                 ← Dependencies (updated)
├── QUICKSTART_DOWNLOAD.md           ← Step-by-step guide
└── DATA_ACQUISITION_SUMMARY.md      ← This file
```

---

## How to Use

### Option 1: Complete Setup (Recommended)
Run everything at once:
```bash
scripts\setup_complete.bat
```

### Option 2: Step by Step
```bash
# 1. Install dependencies
pip install sentinelhub Pillow python-dotenv

# 2. Create directories
python scripts\setup_dirs.py

# 3. Test API
python scripts\test_api.py

# 4. Download imagery
python scripts\download_imagery.py
```

### Option 3: Quick Download (if already set up)
```bash
scripts\run_download.bat
```

---

## Expected Results

### Download Summary
- **Total images:** 12 (6 AOIs × 2 dates)
- **Total size:** ~50-100 MB
- **Format:** PNG, RGB
- **Resolution:** 10m per pixel
- **Image size:** 512×512 pixels
- **Duration:** 5-10 minutes

### File Output
```
data/imagery/nyc_manhattan/
├── 2023-01-01.png
└── 2023-06-01.png

data/imagery/nyc_jfk/
├── 2023-01-01.png
└── 2023-06-01.png

... (same for other AOIs)

data/metadata/
└── imagery_metadata.json
```

### Metadata Content
```json
[
  {
    "aoi_id": "nyc_manhattan",
    "aoi_name": "Manhattan Urban Core",
    "bbox": [-74.02, 40.70, -73.92, 40.85],
    "date_range": ["2023-01-01", "2023-01-31"],
    "filename": "2023-01-01.png",
    "path": "data\\imagery\\nyc_manhattan\\2023-01-01.png",
    "source": "Sentinel-2",
    "resolution": "10m",
    "downloaded_at": "2024-01-15T10:30:00"
  },
  ...
]
```

---

## API Requirements

### Sentinel Hub (Required)
- **Free tier:** 2,500 requests/month
- **Signup:** https://www.sentinel-hub.com/
- **Credentials needed:**
  - Instance ID
  - Client ID
  - Client Secret

### USGS Landsat (Optional)
- **Free:** Unlimited
- **Signup:** https://earthexplorer.usgs.gov/
- **Credentials needed:**
  - Username
  - Password
- **Note:** Currently not used, Sentinel-2 is primary source

---

## Troubleshooting

### Problem: sentinelhub not installed
```bash
pip install sentinelhub
```

### Problem: Authentication failed
1. Check .env file has all three Sentinel Hub credentials
2. Verify at: https://apps.sentinel-hub.com/dashboard/
3. Try regenerating OAuth Client

### Problem: No images found
- Some dates may have high cloud cover
- Script will skip and continue
- Try different dates in `DATE_RANGES`

### Problem: Rate limit exceeded
- Free tier: 2,500 req/month
- Wait for reset or upgrade

---

## Customization

### Add New AOI
Edit `AOIS` dict in `download_imagery.py`:
```python
'my_custom_aoi': {
    'name': 'My Custom Area',
    'bbox': [lon_min, lat_min, lon_max, lat_max],
    'description': 'Custom area description',
    'mgrs': 'GRID_CODE'
}
```

### Change Dates
Edit `DATE_RANGES`:
```python
DATE_RANGES = [
    ('2024-01-01', '2024-01-31'),
    ('2024-06-01', '2024-06-30')
]
```

### Adjust Image Size
Change `IMAGE_SIZE`:
```python
IMAGE_SIZE = [1024, 1024]  # Larger images
```

### Adjust Cloud Cover
Change `MAX_CLOUD_COVER`:
```python
MAX_CLOUD_COVER = 20  # More lenient (0-100)
```

---

## Next Steps

After successful download:

1. ✓ **Verify downloads:** Check `data/imagery/` folders
2. ✓ **Check metadata:** Review `data/metadata/imagery_metadata.json`
3. → **Preprocess imagery:** Run building detection (next phase)
4. → **Start web app:** Launch ASIP application
5. → **Test features:** Upload images, detect buildings

---

## Summary

All scripts and documentation are ready for satellite imagery acquisition. Your API keys are configured in `.env`, and you can now:

1. **Test the connection** with `scripts\test_api.bat`
2. **Download imagery** with `scripts\run_download.bat`
3. **Or do everything** with `scripts\setup_complete.bat`

The system will download 12 high-resolution satellite images covering key urban and infrastructure areas in New York and Tehran, ready for building detection and analysis in your ASIP application.

---

**Status:** Setup complete! Ready to download imagery. 🛰️
