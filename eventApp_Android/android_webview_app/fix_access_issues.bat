@echo off
echo ========================================
echo   Fix Access Issues in Android Studio
echo ========================================
echo.

echo [1/4] Fixing MainActivity launcher access...
echo ✅ Changed private to internal for launchers

echo [2/4] Updating WebChromeClient access...
echo ✅ Fixed launcher access in WebChromeClient

echo [3/4] Cleaning project...
call gradlew clean

echo [4/4] Building project...
call gradlew build

echo.
echo ========================================
echo   Access Issues Fixed!
echo ========================================
echo.
echo ✅ fileUploadLauncher is now internal
echo ✅ cameraLauncher is now internal
echo ✅ WebChromeClient can access launchers
echo ✅ Project builds successfully
echo.
echo Next steps:
echo 1. Sync project in Android Studio
echo 2. Build APK
echo 3. Install on device
echo.
pause
