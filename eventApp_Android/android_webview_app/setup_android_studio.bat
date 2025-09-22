@echo off
echo ========================================
echo    EventApp Android WebView - Setup
echo ========================================
echo.

echo [1/5] Checking Android Studio installation...
where android-studio >nul 2>&1
if errorlevel 1 (
    echo WARNING: Android Studio not found in PATH
    echo Please install Android Studio from: https://developer.android.com/studio
    echo.
) else (
    echo ✅ Android Studio found
)

echo [2/5] Checking Java installation...
java -version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Java not found
    echo Please install Java JDK 8 or higher
    echo.
) else (
    echo ✅ Java found
)

echo [3/5] Checking Android SDK...
if exist "%ANDROID_HOME%\platform-tools\adb.exe" (
    echo ✅ Android SDK found
) else (
    echo WARNING: Android SDK not found
    echo Please set ANDROID_HOME environment variable
    echo.
)

echo [4/5] Creating project structure...
if not exist "app\src\main\java\com\eventapp\webview" (
    mkdir "app\src\main\java\com\eventapp\webview"
    echo ✅ Created Java package directory
)

if not exist "app\src\main\res\layout" (
    mkdir "app\src\main\res\layout"
    echo ✅ Created layout directory
)

if not exist "app\src\main\res\values" (
    mkdir "app\src\main\res\values"
    echo ✅ Created values directory
)

if not exist "app\src\main\res\xml" (
    mkdir "app\src\main\res\xml"
    echo ✅ Created xml directory
)

echo [5/5] Setup complete!
echo.
echo ========================================
echo   Next Steps:
echo ========================================
echo.
echo 1. Open Android Studio
echo 2. Open this project folder
echo 3. Wait for Gradle sync
echo 4. Connect Android device or start emulator
echo 5. Click "Run" button
echo.
echo ========================================
echo   Configuration:
echo ========================================
echo.
echo - Flask server URL: http://192.168.68.116:3000
echo - Package name: com.eventapp.webview
echo - Min SDK: 24 (Android 7.0)
echo - Target SDK: 34 (Android 14)
echo.
echo ========================================
echo   Setup completed successfully!
echo ========================================
echo.
pause
