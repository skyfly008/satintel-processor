@echo off
REM Download Satellite Imagery for ASIP
echo ========================================
echo ASIP Data Acquisition
echo ========================================
echo.
echo This will download satellite imagery for:
echo - 3 New York AOIs
echo - 3 Tehran AOIs
echo - 2 date ranges per AOI
echo.
echo Expected download: ~12 images, ^<100MB
echo.
pause

cd /d "%~dp0.."

echo.
echo Checking dependencies...
python -c "import sentinelhub" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo sentinelhub not installed. Installing...
    pip install sentinelhub Pillow
)

echo.
echo Starting download...
echo.
python scripts\download_imagery.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Download complete!
    echo Check: data\imagery\
    echo ========================================
) else (
    echo.
    echo ========================================
    echo Download failed. Check errors above.
    echo ========================================
)

pause
