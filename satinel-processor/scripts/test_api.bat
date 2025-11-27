@echo off
REM Test Sentinel Hub API Connection
echo Testing Sentinel Hub API connection...
echo.

cd /d "%~dp0.."
python scripts\test_api.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Connection test successful!
    echo You can now run: run_download.bat
    echo ========================================
) else (
    echo.
    echo ========================================
    echo Connection test failed.
    echo Please check your .env file.
    echo ========================================
)

pause
