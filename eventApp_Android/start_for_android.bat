@echo off
echo ========================================
echo    EventApp - Android PWA Launcher
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

echo [1/3] Activating virtual environment...
call venv\Scripts\activate.bat

echo [2/3] Checking dependencies...
python -c "import flask, flask_sqlalchemy, flask_login, werkzeug, qrcode, PIL, dotenv" 2>nul
if errorlevel 1 (
    echo WARNING: Some dependencies might be missing.
    echo Installing requirements...
    pip install -r requirements.txt
)

echo [3/3] Starting EventApp for Android...
echo.
echo ========================================
echo   EventApp is starting for Android...
echo ========================================
echo.

:: Get IP address
echo Finding your computer's IP address...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
    set "ip=%%a"
    goto :found
)
:found
set "ip=%ip: =%"

echo.
echo ========================================
echo   Android Access Information
echo ========================================
echo.
echo Your computer's IP address: %ip%
echo.
echo To access from Android device:
echo 1. Connect Android to SAME WiFi network
echo 2. Open Chrome browser on Android
echo 3. Navigate to: http://%ip%:5001
echo 4. Look for "Install App" button
echo 5. Tap "Install App" to install PWA
echo.
echo For Android Studio Emulator:
echo - Use: http://10.0.2.2:5001
echo.
echo ========================================
echo   Starting EventApp...
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
