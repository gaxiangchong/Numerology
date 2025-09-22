@echo off
echo Fixing Gradle download issues...
echo.

echo Step 1: Clearing Gradle cache...
rmdir /s /q "%USERPROFILE%\.gradle\wrapper\dists" 2>nul
rmdir /s /q "%USERPROFILE%\.gradle\caches" 2>nul

echo Step 2: Creating Gradle directories...
mkdir "%USERPROFILE%\.gradle\wrapper\dists\gradle-7.6.1-all" 2>nul

echo Step 3: Downloading Gradle manually...
echo Please download gradle-7.6.1-all.zip from:
echo https://services.gradle.org/distributions/gradle-7.6.1-all.zip
echo.
echo Save it to: %USERPROFILE%\.gradle\wrapper\dists\gradle-7.6.1-all\
echo.
echo Then run: npx cap open android
pause
