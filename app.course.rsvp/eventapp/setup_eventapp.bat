@echo off
echo ========================================
echo        EventApp Setup Utility
echo ========================================
echo.

:: Change to the script directory
cd /d "%~dp0"

:: Check if we're in the right directory
if not exist "app.py" (
    echo ERROR: app.py not found!
    echo Please make sure you're in the correct directory.
    echo Expected: D:\GitHub\app.course.rsvp\eventapp
    echo.
    pause
    exit /b 1
)

echo [1/4] Activating virtual environment...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo Virtual environment activated.
) else (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Virtual environment created and activated.
)

echo [2/4] Installing dependencies...
pip install -r requirements.txt

echo [3/4] Setting up database...
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database tables created successfully!')"

echo [4/4] Creating admin user...
echo.
echo You will now be prompted to create an admin user.
echo This is required to access admin features like creating events.
echo.
python setup_admin.py

echo.
echo ========================================
echo        Setup Complete!
echo ========================================
echo.
echo You can now run EventApp using:
echo 1. Double-click "run_eventapp.bat"
echo 2. Or manually: python app.py
echo.
echo The app will be available at: http://127.0.0.1:5001
echo.
pause
