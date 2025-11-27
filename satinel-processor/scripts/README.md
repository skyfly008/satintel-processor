# Scripts Directory

This directory contains utility scripts for the ASIP project.

## Available Scripts

### 1. API Connection Test
**File:** `test_api.py` / `test_api.bat`

Test your Sentinel Hub API credentials before downloading imagery.

**Usage:**
```bash
# Windows
scripts\test_api.bat

# Python directly
python scripts\test_api.py
```

**What it checks:**
- ✓ .env file has all required credentials
- ✓ sentinelhub package is installed
- ✓ API credentials are valid
- ✓ Can connect to Sentinel Hub API
- ✓ Can retrieve test imagery

---

### 2. Download Imagery
**File:** `download_imagery.py` / `run_download.bat`

Download satellite imagery for all predefined Areas of Interest (AOIs).

**Usage:**
```bash
# Windows (recommended)
scripts\run_download.bat

# Python directly
python scripts\download_imagery.py
```

**Downloads:**
- 6 AOIs (3 New York + 3 Tehran)
- 2 date ranges per AOI (Jan 2023, Jun 2023)
- ~12 images total
- <100MB storage
- 10m resolution (Sentinel-2)

**Output:**
```
data/imagery/
├── nyc_manhattan/
│   ├── 2023-01-01.png
│   └── 2023-06-01.png
├── nyc_jfk/
├── nyc_industrial/
├── tehran_central/
├── tehran_airport/
└── tehran_industrial/
```

---

## Quick Start Guide

### Step 1: Verify Setup
```bash
# Make sure .env file has your API keys
# Check: SENTINEL_INSTANCE_ID, SENTINEL_CLIENT_ID, SENTINEL_CLIENT_SECRET
```

### Step 2: Install Dependencies
```bash
pip install sentinelhub Pillow
```

### Step 3: Test Connection
```bash
scripts\test_api.bat
```

### Step 4: Download Imagery
```bash
scripts\run_download.bat
```

### Step 5: Verify Download
```bash
# Check the data/imagery folder
dir data\imagery\nyc_manhattan
```

---

## Detailed Documentation

For complete documentation on data acquisition, see:
- **[DATA_ACQUISITION.md](DATA_ACQUISITION.md)** - Full guide with troubleshooting

---

## Requirements

### Required Packages
```
sentinelhub>=3.9.0
Pillow>=10.0.0
python-dotenv>=1.0.0
```

### API Credentials
- **Sentinel Hub:** https://www.sentinel-hub.com/
  - Instance ID
  - Client ID  
  - Client Secret

### Optional (Landsat fallback)
```
landsatxplore>=0.14.0
rasterio>=1.3.9
```

---

## Troubleshooting

### Import Error: No module named 'sentinelhub'
```bash
pip install sentinelhub
```

### Authentication Failed
1. Check `.env` file has correct credentials
2. Verify at https://apps.sentinel-hub.com/dashboard/
3. Ensure client ID and secret are active

### No Cloud-Free Images Found
- Try different date ranges
- Increase `MAX_CLOUD_COVER` in download_imagery.py
- Check different seasons (summer usually clearer)

### Rate Limit Exceeded
- Sentinel Hub free tier: 2,500 requests/month
- Wait for quota reset or upgrade plan
- Script includes built-in retry logic

---

## Customization

### Add New AOIs
Edit `AOIS` dictionary in `download_imagery.py`:
```python
'custom_aoi': {
    'name': 'Custom Area',
    'bbox': [lon_min, lat_min, lon_max, lat_max],
    'description': 'My custom area',
    'mgrs': 'GRID_CODE'
}
```

### Change Dates
Edit `DATE_RANGES` in `download_imagery.py`:
```python
DATE_RANGES = [
    ('2024-01-01', '2024-01-31'),
    ('2024-06-01', '2024-06-30')
]
```

### Adjust Image Size
```python
IMAGE_SIZE = [1024, 1024]  # Larger tiles
```

---

## Support

For issues or questions:
1. Check **DATA_ACQUISITION.md** for detailed troubleshooting
2. Verify API credentials at Sentinel Hub dashboard
3. Check Python environment has all dependencies
4. Review error messages from scripts

---

## Next Steps

After downloading imagery:
1. ✓ Verify images in `data/imagery/` folders
2. ✓ Check metadata in `data/metadata/imagery_metadata.json`
3. → Run building detection preprocessing (coming next)
4. → Start ASIP web application
