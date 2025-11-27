@echo off
REM Complete setup for ASIP data acquisition
echo ========================================
echo ASIP Data Acquisition - Complete Setup
echo ========================================
echo.

cd /d "%~dp0.."

echo Step 1/4: Installing dependencies...
pip install sentinelhub Pillow python-dotenv --quiet
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)
echo   Done!
echo.

echo Step 2/4: Creating directory structure...
python scripts\setup_dirs.py
echo.

echo Step 3/4: Testing API connection...
python scripts\test_api.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================
    echo API test failed! Please check:
    echo - Your .env file has correct credentials
    echo - You have internet connection
    echo ========================================
    pause
    exit /b 1
)
echo.

echo Step 4/4: Starting imagery download...
echo This will take 5-10 minutes...
echo.
pause
python scripts\download_imagery.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo SUCCESS! All steps completed.
    echo.
    echo Downloaded imagery is in: data\imagery\
    echo Metadata is in: data\metadata\
    echo.
    echo Next: Run the ASIP web application
    echo ========================================
) else (
    echo.
    echo ========================================
    echo Download failed. Check errors above.
    echo ========================================
)

pause
