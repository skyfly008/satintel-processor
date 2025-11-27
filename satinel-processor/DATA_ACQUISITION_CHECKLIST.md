# Data Acquisition Checklist

## Pre-Download Checklist

### 1. Environment Setup
- [x] .env file exists
- [x] .env has SENTINEL_INSTANCE_ID
- [x] .env has SENTINEL_CLIENT_ID  
- [x] .env has SENTINEL_CLIENT_SECRET
- [ ] Python 3.8+ installed (`python --version`)
- [ ] pip is working (`pip --version`)

### 2. Dependencies
- [ ] sentinelhub installed (`pip install sentinelhub`)
- [ ] Pillow installed (`pip install Pillow`)
- [ ] python-dotenv installed (`pip install python-dotenv`)

**Quick install all:**
```bash
pip install sentinelhub Pillow python-dotenv
```

### 3. Directory Structure
- [ ] data/imagery/ exists
- [ ] data/imagery/nyc_manhattan/ exists
- [ ] data/imagery/nyc_jfk/ exists
- [ ] data/imagery/nyc_industrial/ exists
- [ ] data/imagery/tehran_central/ exists
- [ ] data/imagery/tehran_airport/ exists
- [ ] data/imagery/tehran_industrial/ exists
- [ ] data/metadata/ exists

**Quick create all:**
```bash
python scripts\setup_dirs.py
```

### 4. API Connection Test
- [ ] API test passes (`python scripts\test_api.py`)
- [ ] Can retrieve test image
- [ ] No authentication errors

**Quick test:**
```bash
scripts\test_api.bat
```

---

## Download Checklist

### 5. Run Download
- [ ] Download script started (`python scripts\download_imagery.py`)
- [ ] No errors during download
- [ ] Script completed successfully

**Quick download:**
```bash
scripts\run_download.bat
```

### 6. Verify Results
- [ ] 12 images downloaded (2 per AOI)
- [ ] All images are valid PNG files
- [ ] Total size is reasonable (~50-100MB)
- [ ] imagery_metadata.json created

**Quick verify:**
```bash
dir data\imagery\nyc_manhattan
dir data\imagery\nyc_jfk
dir data\imagery\nyc_industrial
dir data\imagery\tehran_central
dir data\imagery\tehran_airport
dir data\imagery\tehran_industrial
```

---

## Post-Download Checklist

### 7. Quality Check
- [ ] Open a few images to verify they're valid
- [ ] Images show correct geographic areas
- [ ] No corrupted files
- [ ] Metadata has correct information

**Quick visual check:**
```bash
# Open an image
start data\imagery\nyc_manhattan\2023-01-01.png
```

### 8. Documentation
- [ ] Read QUICKSTART_DOWNLOAD.md
- [ ] Read DATA_ACQUISITION_SUMMARY.md
- [ ] Understand how to customize AOIs/dates
- [ ] Know how to troubleshoot issues

---

## Troubleshooting Checklist

### If API Test Fails:
- [ ] Check .env file has correct credentials
- [ ] Verify credentials at Sentinel Hub dashboard
- [ ] Check internet connection
- [ ] Try regenerating OAuth client in dashboard

### If Download Fails:
- [ ] Check error message
- [ ] Verify API quota not exceeded
- [ ] Try different date ranges
- [ ] Increase MAX_CLOUD_COVER setting

### If No Images Found:
- [ ] This is normal for some dates
- [ ] Script should continue with other AOIs
- [ ] Try different seasons (summer is clearer)
- [ ] Adjust date ranges in script

---

## One-Click Setup (Recommended)

Skip all manual steps and run:
```bash
scripts\setup_complete.bat
```

This will:
1. ✓ Install dependencies
2. ✓ Create directories
3. ✓ Test API connection
4. ✓ Download all imagery

---

## Success Criteria

Your setup is complete when:
- ✓ API test passes without errors
- ✓ 12 images downloaded to correct folders
- ✓ imagery_metadata.json exists with 12 entries
- ✓ Total download size is 50-100 MB
- ✓ Images open correctly in image viewer

---

## Next Phase: Building Detection

After completing this checklist:
1. → Prepare building detection model
2. → Preprocess imagery for inference
3. → Generate building masks
4. → Integrate with web application

---

## Quick Commands Reference

```bash
# Complete setup (do everything)
scripts\setup_complete.bat

# Test API only
scripts\test_api.bat

# Download imagery only
scripts\run_download.bat

# Create directories only
python scripts\setup_dirs.py

# Check what's downloaded
dir data\imagery\* /s

# View metadata
type data\metadata\imagery_metadata.json

# Install dependencies
pip install sentinelhub Pillow python-dotenv
```

---

**Current Status:** Ready to start data acquisition! 🚀
