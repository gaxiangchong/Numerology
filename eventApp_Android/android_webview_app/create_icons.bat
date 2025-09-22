@echo off
echo ========================================
echo    Creating Android Launcher Icons
echo ========================================
echo.

echo [1/2] Installing Pillow (if needed)...
pip install Pillow

echo [2/2] Creating launcher icons...
python create_launcher_icons.py

echo.
echo ========================================
echo   Launcher Icons Created Successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Refresh Android Studio project
echo 2. Build the APK
echo 3. Install on device
echo.
pause
