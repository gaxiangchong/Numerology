@echo off
echo ========================================
echo    Android Studio Emulator Setup
echo ========================================
echo.

echo This guide will help you set up Android Studio emulator
echo to test your EventApp PWA.
echo.

echo ========================================
echo   Step 1: Open Android Studio
echo ========================================
echo.
echo 1. Launch Android Studio
echo 2. Go to Tools → AVD Manager
echo 3. Click "Create Virtual Device"
echo.

echo ========================================
echo   Step 2: Create Virtual Device
echo ========================================
echo.
echo 1. Choose "Phone" category
echo 2. Select "Pixel 4" or "Pixel 5"
echo 3. Click "Next"
echo.

echo ========================================
echo   Step 3: Select System Image
echo ========================================
echo.
echo 1. Choose "API 30" or "API 31" (Android 11/12)
echo 2. Click "Download" if needed
echo 3. Click "Next" after download
echo.

echo ========================================
echo   Step 4: Configure AVD
echo ========================================
echo.
echo 1. Name: "EventApp_Emulator"
echo 2. Click "Finish"
echo.

echo ========================================
echo   Step 5: Start Emulator
echo ========================================
echo.
echo 1. Click ▶️ Play button next to your device
echo 2. Wait for emulator to boot (2-3 minutes)
echo 3. You'll see Android home screen
echo.

echo ========================================
echo   Step 6: Access EventApp
echo ========================================
echo.
echo 1. In emulator, open Chrome browser
echo 2. Navigate to: http://10.0.2.2:5001
echo 3. Look for "Install App" button
echo 4. Tap "Install App" to install PWA
echo.

echo ========================================
echo   Troubleshooting
echo ========================================
echo.
echo If "Install App" button doesn't appear:
echo 1. Go to chrome://flags/
echo 2. Search for "Desktop PWA"
echo 3. Enable "Desktop PWA install"
echo 4. Restart Chrome
echo.

echo If connection fails:
echo 1. Check that EventApp is running
echo 2. Use http://10.0.2.2:5001 (not your IP)
echo 3. Check Windows Firewall settings
echo.

echo ========================================
echo   Ready to Start?
echo ========================================
echo.
echo Press any key to continue to the next step...
pause >nul

echo.
echo Now run: start_for_android.bat
echo This will start your EventApp for Android testing.
echo.
pause
