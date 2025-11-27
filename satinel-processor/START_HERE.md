# 🛰️ ASIP Data Acquisition - Ready to Go!

## ✅ What's Been Set Up

I've created a complete satellite imagery acquisition system for your ASIP project. Here's what's ready:

### 📦 Files Created

#### Core Scripts (in `scripts/`)
1. **download_imagery.py** - Main script to download Sentinel-2 imagery
2. **test_api.py** - Test your API connection before downloading
3. **setup_dirs.py** - Create required directory structure

#### Windows Batch Files (in `scripts/`)
1. **setup_complete.bat** - ONE-CLICK SETUP (recommended!)
2. **run_download.bat** - Download imagery only
3. **test_api.bat** - Test API connection only

#### Documentation
1. **QUICKSTART_DOWNLOAD.md** - Step-by-step guide with troubleshooting
2. **DATA_ACQUISITION_SUMMARY.md** - Complete overview of the system
3. **DATA_ACQUISITION_CHECKLIST.md** - Checklist to track your progress
4. **scripts/README.md** - Scripts overview
5. **scripts/DATA_ACQUISITION.md** - Detailed technical documentation

### 🗺️ Areas of Interest (Predownload Strategy)

#### New York (3 AOIs)
- **Manhattan**: Dense urban buildings (40.70-40.85°N, 74.02-73.92°W)
- **JFK Airport**: Infrastructure (40.62-40.66°N, 73.82-73.76°W)  
- **Industrial Brooklyn**: Warehouses (40.65-40.70°N, 73.95-73.90°W)

#### Tehran (3 AOIs)
- **Central Urban**: Residential/commercial (35.68-35.75°N, 51.35-51.45°E)
- **Airport**: Airfield infrastructure (35.40-35.45°N, 51.10-51.20°E)
- **Industrial**: Factories (35.65-35.70°N, 51.25-51.35°E)

### 📊 Download Specs
- **Images per AOI**: 2 (January 2023 & June 2023)
- **Total images**: 12
- **Resolution**: 10m per pixel (Sentinel-2)
- **Image size**: 512×512 pixels
- **Total size**: ~50-100 MB
- **Format**: PNG, RGB
- **Cloud cover**: <10%

### 🔧 Configuration Updates

**Updated `.env`** with:
```
SENTINEL_INSTANCE_ID=1e39c110-d06c-4608-8da9-789f0c98dbe6
SENTINEL_CLIENT_ID=f8ac55c1-d076-4b2d-8751-68bc139dc8a5
SENTINEL_CLIENT_SECRET=M9Yc6ju1EOXpTC2hD0R9Tb1wwqzKfXt2
USGS_USERNAME=
USGS_PASSWORD=
```

**Updated `requirements.txt`** with:
```
sentinelhub==3.9.0
landsatxplore==0.14.0
rasterio==1.3.9
```

**Updated `README.md`** with download instructions.

---

## 🚀 How to Use (3 Options)

### Option 1: ONE-CLICK SETUP (Easiest!)
```bash
scripts\setup_complete.bat
```
This does everything:
1. Installs dependencies
2. Creates directories
3. Tests API
4. Downloads imagery

### Option 2: Step-by-Step
```bash
# 1. Install packages
pip install sentinelhub Pillow python-dotenv

# 2. Create directories
python scripts\setup_dirs.py

# 3. Test API
scripts\test_api.bat

# 4. Download imagery
scripts\run_download.bat
```

### Option 3: Just Download (if already set up)
```bash
scripts\run_download.bat
```

---

## 📁 What You'll Get

### Directory Structure After Download
```
data/
├── imagery/
│   ├── nyc_manhattan/
│   │   ├── 2023-01-01.png      ← Satellite image
│   │   └── 2023-06-01.png
│   ├── nyc_jfk/
│   │   ├── 2023-01-01.png
│   │   └── 2023-06-01.png
│   ├── nyc_industrial/
│   │   ├── 2023-01-01.png
│   │   └── 2023-06-01.png
│   ├── tehran_central/
│   │   ├── 2023-01-01.png
│   │   └── 2023-06-01.png
│   ├── tehran_airport/
│   │   ├── 2023-01-01.png
│   │   └── 2023-06-01.png
│   └── tehran_industrial/
│       ├── 2023-01-01.png
│       └── 2023-06-01.png
└── metadata/
    └── imagery_metadata.json    ← Download metadata
```

### Metadata Example
```json
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
}
```

---

## ⏱️ Timeline

1. **API Test**: 1 minute
2. **Full Download**: 5-10 minutes (12 images)
3. **Total Time**: ~10 minutes from start to finish

---

## 🔍 Verification

After download completes, check:

```bash
# List downloaded files
dir data\imagery\nyc_manhattan
dir data\imagery\nyc_jfk
dir data\imagery\nyc_industrial
dir data\imagery\tehran_central
dir data\imagery\tehran_airport
dir data\imagery\tehran_industrial

# View metadata
type data\metadata\imagery_metadata.json

# Open an image
start data\imagery\nyc_manhattan\2023-01-01.png
```

---

## 📚 Documentation Guide

Start here based on your needs:

1. **Just want to download?** → Run `scripts\setup_complete.bat`
2. **Need step-by-step?** → Read `QUICKSTART_DOWNLOAD.md`
3. **Want full details?** → Read `DATA_ACQUISITION_SUMMARY.md`
4. **Track progress?** → Use `DATA_ACQUISITION_CHECKLIST.md`
5. **Troubleshooting?** → Check `scripts/DATA_ACQUISITION.md`

---

## 🛠️ Troubleshooting Quick Reference

### Problem: API test fails
**Solution:** Check .env file has correct credentials

### Problem: sentinelhub not installed
**Solution:** `pip install sentinelhub`

### Problem: No images found
**Normal!** Some dates have cloud cover, script continues

### Problem: Rate limit exceeded
**Solution:** Free tier is 2,500 req/month, wait or upgrade

### Problem: Download is slow
**Normal!** Takes 5-10 minutes for all images

---

## 🎯 Next Steps

After successful download:

1. ✅ **Verify downloads** in `data/imagery/` folders
2. ✅ **Check metadata** in `data/metadata/`
3. → **Build detection preprocessing** (next phase)
4. → **Start ASIP web app**
5. → **Test building detection**

---

## 🎨 Customization

### Add More AOIs
Edit `AOIS` in `download_imagery.py`:
```python
'my_aoi': {
    'name': 'Custom Area',
    'bbox': [lon_min, lat_min, lon_max, lat_max],
    'description': 'Description',
    'mgrs': 'GRID'
}
```

### Different Dates
Edit `DATE_RANGES`:
```python
DATE_RANGES = [
    ('2024-01-01', '2024-01-31'),
    ('2024-06-01', '2024-06-30')
]
```

### Larger Images
Change `IMAGE_SIZE`:
```python
IMAGE_SIZE = [1024, 1024]
```

---

## 📋 Quick Commands

```bash
# Complete setup
scripts\setup_complete.bat

# Test API
scripts\test_api.bat

# Download only
scripts\run_download.bat

# Manual steps
pip install sentinelhub Pillow python-dotenv
python scripts\setup_dirs.py
python scripts\test_api.py
python scripts\download_imagery.py
```

---

## ✅ Success Criteria

Your setup is successful when:
- ✅ API test passes
- ✅ 12 images downloaded
- ✅ imagery_metadata.json created
- ✅ Images open correctly
- ✅ Total size ~50-100 MB

---

## 🔗 Resources

- **Sentinel Hub**: https://www.sentinel-hub.com/
- **Sentinel Hub Dashboard**: https://apps.sentinel-hub.com/dashboard/
- **Sentinel Hub Docs**: https://docs.sentinel-hub.com/
- **USGS EarthExplorer**: https://earthexplorer.usgs.gov/

---

## 📝 Summary

Everything is ready for you to download satellite imagery! Your API keys are configured, scripts are created, and documentation is complete. 

**To get started right now:**
```bash
scripts\setup_complete.bat
```

That's it! The script will handle everything automatically.

---

**Status: 🟢 READY TO DOWNLOAD**

Your ASIP project now has a complete data acquisition pipeline that will download high-resolution satellite imagery for 6 strategic areas of interest. The images will be perfect for building detection, infrastructure analysis, and demonstrating your geospatial intelligence capabilities.

Happy downloading! 🛰️✨
