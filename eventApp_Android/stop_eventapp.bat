@echo off
echo ========================================
echo        Stopping EventApp
echo ========================================
echo.

:: Kill any running Python processes (EventApp)
taskkill /f /im python.exe 2>nul

if errorlevel 1 (
    echo No EventApp processes found running.
) else (
    echo EventApp stopped successfully.
)

echo.
echo You can now safely close this window.
echo.
pause
