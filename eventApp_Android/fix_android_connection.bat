@echo off
echo ========================================
echo    Fixing Android Connection Issues
echo ========================================
echo.

echo Your IP address is: 192.168.68.116
echo Your app is running on port 5001
echo.

echo ========================================
echo   Step 1: Check Windows Firewall
echo ========================================
echo.

echo Adding Windows Firewall exception for port 5001...
netsh advfirewall firewall add rule name="EventApp PWA" dir=in action=allow protocol=TCP localport=5001

echo.
echo ========================================
echo   Step 2: Test Connection
echo ========================================
echo.

echo Testing if your app is accessible...
curl -s http://192.168.68.116:5001 >nul 2>&1
if errorlevel 1 (
    echo ERROR: Cannot access app from localhost
    echo This might be a firewall issue.
    echo.
    echo Try these solutions:
    echo 1. Temporarily disable Windows Firewall
    echo 2. Use a different port (8080)
    echo 3. Check if antivirus is blocking
) else (
    echo SUCCESS: App is accessible locally
    echo.
    echo Now try on your Android device:
    echo http://192.168.68.116:5001
)

echo.
echo ========================================
echo   Step 3: Alternative Solutions
echo ========================================
echo.

echo If still not working, try these:
echo.
echo 1. TEMPORARILY disable Windows Firewall:
echo    - Go to Windows Security
echo    - Firewall & network protection
echo    - Turn off for private networks
echo.
echo 2. Use a different port:
echo    - Change port to 8080 in app.py
echo    - Access via http://192.168.68.116:8080
echo.
echo 3. Check antivirus software:
echo    - Some antivirus blocks local connections
echo    - Add exception for Python/Flask
echo.

echo ========================================
echo   Step 4: Test URLs
echo ========================================
echo.

echo Try these URLs on your Android device:
echo.
echo Primary: http://192.168.68.116:5001
echo Alternative: http://192.168.68.116:8080
echo.
echo If using Android Studio emulator:
echo Emulator: http://10.0.2.2:5001
echo.

echo ========================================
echo   Step 5: Quick Test
echo ========================================
echo.

echo Opening browser to test connection...
start http://192.168.68.116:5001

echo.
echo If the browser opens your app, then the issue is:
echo - Android device not on same network
echo - Android device firewall/security settings
echo.
echo If the browser shows "Not Found", then:
echo - Windows Firewall is blocking
echo - Try the solutions above
echo.

pause
