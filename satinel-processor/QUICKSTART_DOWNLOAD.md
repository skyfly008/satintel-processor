# Quick Start: Data Acquisition

## Prerequisites Checklist

- [x] .env file filled with API keys
- [ ] Python packages installed
- [ ] Directory structure created
- [ ] API connection tested
- [ ] Imagery downloaded

## Step-by-Step Instructions

### 1. Install Required Packages (5 minutes)

Open Command Prompt or PowerShell in the project directory:

```bash
cd c:\Users\ML05\Projects\ASIP\satinel-processor
pip install sentinelhub Pillow python-dotenv
```

**Verify installation:**
```bash
python -c "import sentinelhub; print('sentinelhub:', sentinelhub.__version__)"
```

---

### 2. Setup Directory Structure (30 seconds)

```bash
python scripts\setup_dirs.py
```

This creates:
```
data/
├── imagery/
│   ├── nyc_manhattan/
│   ├── nyc_jfk/
│   ├── nyc_industrial/
│   ├── tehran_central/
│   ├── tehran_airport/
│   └── tehran_industrial/
├── masks/
├── cache/
└── metadata/
```

---

### 3. Test API Connection (1 minute)

**Option A: Using batch file (Windows)**
```bash
scripts\test_api.bat
```

**Option B: Using Python directly**
```bash
python scripts\test_api.py
```

**Expected output:**
```
========================================
Sentinel Hub API Connection Test
========================================

1. Checking credentials in .env file...
   ✓ Instance ID: 1e39c110...
   ✓ Client ID: f8ac55c1...
   ✓ Client Secret: ********************

2. Checking if sentinelhub package is installed...
   ✓ sentinelhub version: 3.9.0

3. Configuring Sentinel Hub client...
   ✓ Configuration successful

4. Testing API connection with a small request...
   → Sending test request to Sentinel Hub API...
   ✓ API connection successful!
   ✓ Retrieved test image: (64, 64, 3)

========================================
✓ All tests passed! Ready to download imagery.
========================================
```

**If test fails:** Check troubleshooting section below.

---

### 4. Download Satellite Imagery (5-10 minutes)

**Option A: Using batch file (Windows)**
```bash
scripts\run_download.bat
```

**Option B: Using Python directly**
```bash
python scripts\download_imagery.py
```

**What happens:**
- Downloads 2 images per AOI (6 AOIs = 12 images)
- Each image: 512×512 pixels, 10m resolution
- Saves as PNG files in respective folders
- Creates metadata JSON file
- Shows progress and summary

**Expected output:**
```
========================================
ASIP Data Acquisition Script
========================================

Setting up directory structure...
  Created: data\imagery\nyc_manhattan
  ...

========================================
Downloading Sentinel-2 Imagery
========================================

Processing AOI: nyc_manhattan (Manhattan Urban Core)
  Date range: 2023-01-01 to 2023-01-31
    ✓ Downloaded: data\imagery\nyc_manhattan\2023-01-01.png
  Date range: 2023-06-01 to 2023-06-30
    ✓ Downloaded: data\imagery\nyc_manhattan\2023-06-01.png
...

========================================
DOWNLOAD SUMMARY
========================================
nyc_manhattan        : 2 images (5.23 MB)
nyc_jfk              : 2 images (4.87 MB)
...
------------------------------------------------------------
TOTAL                : 12 images (58.45 MB)
========================================

✓ Data acquisition complete!
```

---

### 5. Verify Downloads

Check the downloaded files:

```bash
# List files in one AOI
dir data\imagery\nyc_manhattan

# Check metadata
type data\metadata\imagery_metadata.json
```

You should see:
- `2023-01-01.png` and `2023-06-01.png` in each AOI folder
- `imagery_metadata.json` with details about each download

---

## Troubleshooting

### Issue: "sentinelhub not installed"
**Solution:**
```bash
pip install sentinelhub
```

### Issue: "Authentication failed"
**Solution:**
1. Check your .env file has correct values
2. Verify credentials at: https://apps.sentinel-hub.com/dashboard/
3. Make sure SENTINEL_INSTANCE_ID, SENTINEL_CLIENT_ID, and SENTINEL_CLIENT_SECRET are all set
4. Try regenerating OAuth Client credentials in Sentinel Hub dashboard

### Issue: "No cloud-free images found"
**Solution:**
- This is normal for some dates/locations
- Script will skip and continue with other AOIs
- Try editing `DATE_RANGES` in `download_imagery.py` to different months
- Increase `MAX_CLOUD_COVER` from 10 to 20 or 30

### Issue: "Rate limit exceeded"
**Solution:**
- Sentinel Hub free tier: 2,500 requests/month
- Wait for monthly quota reset
- Or upgrade to paid plan at Sentinel Hub

### Issue: Download is slow
**Solution:**
- Normal! Each image takes 30-60 seconds
- Total download: 5-10 minutes for all 12 images
- Be patient and let it run

---

## File Structure After Download

```
satinel-processor/
├── data/
│   ├── imagery/
│   │   ├── nyc_manhattan/
│   │   │   ├── 2023-01-01.png    ← Satellite image
│   │   │   └── 2023-06-01.png
│   │   ├── nyc_jfk/
│   │   │   ├── 2023-01-01.png
│   │   │   └── 2023-06-01.png
│   │   └── ... (other AOIs)
│   ├── masks/                     ← (Empty for now)
│   ├── cache/                     ← (Empty for now)
│   └── metadata/
│       └── imagery_metadata.json  ← Download metadata
├── scripts/
│   ├── test_api.py
│   ├── download_imagery.py
│   └── ...
└── .env                           ← Your API keys
```

---

## What's Next?

After successful download:

1. ✓ **Imagery downloaded** to `data/imagery/`
2. → **Next:** Run building detection preprocessing
3. → **Next:** Start ASIP web application
4. → **Next:** Test building detection on downloaded images

---

## Additional Resources

- **Full Documentation:** `scripts/DATA_ACQUISITION.md`
- **Scripts README:** `scripts/README.md`
- **Sentinel Hub Docs:** https://docs.sentinel-hub.com/
- **Sentinel Hub Dashboard:** https://apps.sentinel-hub.com/dashboard/

---

## Need Help?

Common commands:

```bash
# Reinstall dependencies
pip install --upgrade sentinelhub Pillow

# Test API again
python scripts\test_api.py

# Re-run download (skips existing files)
python scripts\download_imagery.py

# Check Python version (needs 3.8+)
python --version

# Check installed packages
pip list | findstr sentinel
```

---

**Status:** Ready to download imagery! 🛰️
