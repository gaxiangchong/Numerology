@echo off
echo ========================================
echo    EventApp Debug - Android PWA
echo ========================================
echo.

:: Change to the script directory
cd /d "%~dp0"

:: Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run setup_eventapp.bat first.
    echo.
    pause
    exit /b 1
)

echo [1/2] Activating virtual environment...
call venv\Scripts\activate.bat

echo [2/2] Starting EventApp Debug on port 8080...
echo.

:: Start the debug Flask application
python debug_app.py

:: Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ========================================
    echo   Debug app stopped with an error
    echo ========================================
    echo.
    pause
)
