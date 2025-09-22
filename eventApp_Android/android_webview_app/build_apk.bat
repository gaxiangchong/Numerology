@echo off
echo ========================================
echo    EventApp Android WebView - Build APK
echo ========================================
echo.

:: Check if we're in the right directory
if not exist "app\build.gradle" (
    echo ERROR: Not in the correct directory!
    echo Please run this from the android_webview_app folder.
    echo.
    pause
    exit /b 1
)

echo [1/4] Cleaning previous builds...
call gradlew clean

echo [2/4] Building debug APK...
call gradlew assembleDebug

echo [3/4] Building release APK...
call gradlew assembleRelease

echo [4/4] Build complete!
echo.
echo ========================================
echo   APK Files Generated:
echo ========================================
echo.
echo Debug APK: app\build\outputs\apk\debug\app-debug.apk
echo Release APK: app\build\outputs\apk\release\app-release.apk
echo.
echo ========================================
echo   Installation Instructions:
echo ========================================
echo.
echo 1. Enable "Unknown Sources" on your Android device
echo 2. Transfer APK to your device
echo 3. Install the APK
echo 4. Make sure Flask server is running on 192.168.68.116:3000
echo.
echo ========================================
echo   Build completed successfully!
echo ========================================
echo.
pause
