@echo off
echo ========================================
echo    Fix Gradle Sync Issues
echo ========================================
echo.

echo [1/6] Stopping all Gradle daemons...
call gradlew --stop

echo [2/6] Cleaning project...
call gradlew clean

echo [3/6] Deleting Gradle cache...
if exist "%USERPROFILE%\.gradle\caches" (
    rmdir /s /q "%USERPROFILE%\.gradle\caches"
    echo ✅ Gradle cache deleted
)

echo [4/6] Deleting build directories...
if exist "app\build" (
    rmdir /s /q "app\build"
    echo ✅ App build directory deleted
)
if exist "build" (
    rmdir /s /q "build"
    echo ✅ Project build directory deleted
)

echo [5/6] Deleting .gradle directory...
if exist ".gradle" (
    rmdir /s /q ".gradle"
    echo ✅ .gradle directory deleted
)

echo [6/6] Re-downloading dependencies...
call gradlew build --refresh-dependencies

echo.
echo ========================================
echo   Gradle Sync Fix Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Close Android Studio completely
echo 2. Reopen Android Studio
echo 3. Open this project
echo 4. Wait for Gradle sync to complete
echo.
echo If issues persist:
echo 1. File → Invalidate Caches and Restart
echo 2. Check internet connection
echo 3. Update Android Studio to latest version
echo.
pause

