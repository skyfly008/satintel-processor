@echo off
REM Git commit and push for data acquisition setup

cd /d "%~dp0"

echo ========================================
echo Checking .env is gitignored...
echo ========================================
git check-ignore .env
if %ERRORLEVEL% EQU 0 (
    echo ✓ .env is properly gitignored
) else (
    echo ⚠ WARNING: .env may not be gitignored!
    echo Please verify before continuing.
    pause
)

echo.
echo ========================================
echo Git Status
echo ========================================
git status

echo.
echo ========================================
echo Adding all files...
echo ========================================
git add .

echo.
echo ========================================
echo Committing changes...
echo ========================================
git commit -m "Project restart: Data acquisition pipeline setup

- Created complete satellite imagery download system
- Added scripts for Sentinel-2 API integration
- Implemented 6 AOIs: 3 New York + 3 Tehran locations
- Added comprehensive documentation and guides
- Created one-click setup batch files for Windows
- Updated .env.example, requirements.txt with necessary fields
- Ready to download 12 high-resolution satellite images

New files:
- START_HERE.md - Quick start guide
- QUICKSTART_DOWNLOAD.md - Step-by-step instructions
- DATA_ACQUISITION_SUMMARY.md - Complete overview
- DATA_ACQUISITION_CHECKLIST.md - Progress tracker
- DATA_ACQUISITION_README.md - Quick reference

Scripts:
- scripts/download_imagery.py - Main download script
- scripts/test_api.py - API connection test
- scripts/setup_dirs.py - Directory creation
- scripts/setup_complete.bat - One-click setup
- scripts/run_download.bat - Download only
- scripts/test_api.bat - Test only
- scripts/README.md - Scripts documentation
- scripts/DATA_ACQUISITION.md - Technical guide

Updates:
- .env.example - Updated template with all credential fields
- requirements.txt - Added sentinelhub, landsatxplore, rasterio
- README.md - Updated installation instructions

Status: Ready to download satellite imagery for ASIP project"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================
    echo Nothing to commit or commit failed
    echo ========================================
    pause
    exit /b 1
)

echo.
echo ========================================
echo Pushing to GitHub...
echo ========================================
git push

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo ✓ SUCCESS! Changes pushed to GitHub
    echo ========================================
    echo.
    echo View at: https://github.com/[your-username]/ASIP
) else (
    echo.
    echo ========================================
    echo ✗ Push failed. Common issues:
    echo - Not connected to internet
    echo - No remote repository configured
    echo - Authentication required
    echo ========================================
    echo.
    echo Try manually:
    echo   git remote -v
    echo   git push origin main
)

echo.
pause

