@echo off
echo ========================================
echo    EventApp - Android PWA (Port 8080)
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

:: Check if app.py exists
if not exist "app.py" (
    echo ERROR: app.py not found!
    echo Please make sure you're in the correct directory.
    echo.
    pause
    exit /b 1
)

echo [1/2] Activating virtual environment...
call venv\Scripts\activate.bat

echo [2/2] Starting EventApp on port 8080...
echo.

:: Start the Flask application on port 8080
python run_port8080.py

:: Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ========================================
    echo   EventApp stopped with an error
    echo ========================================
    echo.
    pause
)
