@echo off
echo ========================================
echo           EventApp Launcher
echo ========================================
echo.

:: Change to the script directory
cd /d "%~dp0"

:: Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please make sure you're in the correct directory.
    echo Expected: D:\GitHub\app.course.rsvp\eventapp
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

echo [1/3] Activating virtual environment...
call venv\Scripts\activate.bat

echo [2/3] Checking dependencies...
python -c "import flask, flask_sqlalchemy, flask_login, werkzeug, qrcode, PIL, dotenv" 2>nul
if errorlevel 1 (
    echo WARNING: Some dependencies might be missing.
    echo Installing requirements...
    pip install -r requirements.txt
)

echo [3/3] Starting EventApp...
echo.
echo ========================================
echo   EventApp is starting...
echo   URL: http://127.0.0.1:5001
echo   Press Ctrl+C to stop the server
echo ========================================
echo.

:: Start the Flask application
python app.py

:: Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ========================================
    echo   EventApp stopped with an error
    echo ========================================
    echo.
    pause
)
