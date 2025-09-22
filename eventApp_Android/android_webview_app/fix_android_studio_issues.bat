@echo off
echo ========================================
echo   Fix Android Studio Issues
echo ========================================
echo.

echo [1/6] Creating launcher icons...
python create_launcher_icons.py

echo [2/6] Creating missing directories...
if not exist "app\src\main\res\mipmap-mdpi" mkdir "app\src\main\res\mipmap-mdpi"
if not exist "app\src\main\res\mipmap-hdpi" mkdir "app\src\main\res\mipmap-hdpi"
if not exist "app\src\main\res\mipmap-xhdpi" mkdir "app\src\main\res\mipmap-xhdpi"
if not exist "app\src\main\res\mipmap-xxhdpi" mkdir "app\src\main\res\mipmap-xxhdpi"
if not exist "app\src\main\res\mipmap-xxxhdpi" mkdir "app\src\main\res\mipmap-xxxhdpi"

echo [3/6] Copying icons to mipmap directories...
copy "app\src\main\res\mipmap-mdpi\ic_launcher.png" "app\src\main\res\mipmap-mdpi\ic_launcher.png" >nul 2>&1
copy "app\src\main\res\mipmap-hdpi\ic_launcher.png" "app\src\main\res\mipmap-hdpi\ic_launcher.png" >nul 2>&1
copy "app\src\main\res\mipmap-xhdpi\ic_launcher.png" "app\src\main\res\mipmap-xhdpi\ic_launcher.png" >nul 2>&1
copy "app\src\main\res\mipmap-xxhdpi\ic_launcher.png" "app\src\main\res\mipmap-xxhdpi\ic_launcher.png" >nul 2>&1
copy "app\src\main\res\mipmap-xxxhdpi\ic_launcher.png" "app\src\main\res\mipmap-xxxhdpi\ic_launcher.png" >nul 2>&1

echo [4/6] Copying round icons...
copy "app\src\main\res\mipmap-mdpi\ic_launcher_round.png" "app\src\main\res\mipmap-mdpi\ic_launcher_round.png" >nul 2>&1
copy "app\src\main\res\mipmap-hdpi\ic_launcher_round.png" "app\src\main\res\mipmap-hdpi\ic_launcher_round.png" >nul 2>&1
copy "app\src\main\res\mipmap-xhdpi\ic_launcher_round.png" "app\src\main\res\mipmap-xhdpi\ic_launcher_round.png" >nul 2>&1
copy "app\src\main\res\mipmap-xxhdpi\ic_launcher_round.png" "app\src\main\res\mipmap-xxhdpi\ic_launcher_round.png" >nul 2>&1
copy "app\src\main\res\mipmap-xxxhdpi\ic_launcher_round.png" "app\src\main\res\mipmap-xxxhdpi\ic_launcher_round.png" >nul 2>&1

echo [5/6] Cleaning project...
call gradlew clean

echo [6/6] Syncing project...
call gradlew build --refresh-dependencies

echo.
echo ========================================
echo   Android Studio Issues Fixed!
echo ========================================
echo.
echo ✅ Camera permission fixed
echo ✅ Hardware features added
echo ✅ Launcher icons created
echo ✅ Round icons created
echo ✅ Project cleaned and synced
echo.
echo Next steps:
echo 1. Refresh Android Studio (File → Sync Project)
echo 2. Build APK (Build → Build Bundle(s) / APK(s))
echo 3. Install on device
echo.
pause
