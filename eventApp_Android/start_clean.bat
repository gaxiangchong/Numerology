@echo off
echo ========================================
echo    EventApp - Clean Android Start
echo ========================================
echo.

:: Kill any existing Python processes
taskkill /f /im python.exe 2>nul

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

echo [2/2] Starting EventApp on port 8080...
echo.

:: Get IP address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
    set "ip=%%a"
    goto :found
)
:found
set "ip=%ip: =%"

echo ========================================
echo   Android Access Information
echo ========================================
echo.
echo Your IP address: %ip%
echo.
echo Android URLs:
echo - Real device: http://%ip%:8080
echo - Emulator: http://10.0.2.2:8080
echo.
echo ========================================
echo   Starting EventApp...
echo   Press Ctrl+C to stop the server
echo ========================================
echo.

:: Start the simple test app
python simple_test.py

:: Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ========================================
    echo   EventApp stopped with an error
    echo ========================================
    echo.
    pause
)
