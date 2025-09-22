@echo off
echo ========================================
echo    EventApp - HTTPS PWA (Port 8443)
echo ========================================
echo.

:: Kill any existing Python processes
taskkill /f /im python.exe 2>nul

:: Change to the script directory
cd /d "%~dp0"

:: Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run setup_eventapp.bat first.
    echo.
    pause
    exit /b 1
)

echo [1/2] Activating virtual environment...
call venv\Scripts\activate.bat

echo [2/2] Starting EventApp with HTTPS...
echo.

:: Get IP address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
    set "ip=%%a"
    goto :found
)
:found
set "ip=%ip: =%"

echo ========================================
echo   Android Access Information
echo ========================================
echo.
echo Your IP address: %ip%
echo.
echo Android URLs (HTTPS):
echo - Real device: https://%ip%:8443
echo - Emulator: https://10.0.2.2:8443
echo.
echo NOTE: You may need to accept security certificate
echo.
echo ========================================
echo   Starting EventApp with HTTPS...
echo   Press Ctrl+C to stop the server
echo ========================================
echo.

:: Start the app with HTTPS
python -c "
from flask import Flask
import ssl

app = Flask(__name__)

@app.route('/')
def hello():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>EventApp HTTPS PWA</title>
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
        <link rel=\"manifest\" href=\"/static/manifest.json\">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #1a1a1a; color: white; }
            .container { max-width: 600px; margin: 0 auto; }
            .success { color: #28a745; }
            .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; text-decoration: none; display: inline-block; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class=\"container\">
            <h1>🎉 EventApp HTTPS PWA</h1>
            <p class=\"success\">✅ HTTPS enabled for PWA installation</p>
            <p class=\"success\">✅ Install App button should appear</p>
            
            <h2>📱 PWA Installation</h2>
            <p>Look for \"Install App\" button in bottom-right corner</p>
            <p>Or use Chrome menu → \"Add to Home screen\"</p>
            
            <h3>🔗 Test Links:</h3>
            <a href=\"/static/manifest.json\" class=\"btn\">PWA Manifest</a>
            <a href=\"/static/sw.js\" class=\"btn\">Service Worker</a>
        </div>
        
        <script>
            // Register service worker
            if ('serviceWorker' in navigator) {
                navigator.serviceWorker.register('/static/sw.js');
            }
            
            // PWA install prompt
            let deferredPrompt;
            window.addEventListener('beforeinstallprompt', (e) => {
                e.preventDefault();
                deferredPrompt = e;
                console.log('PWA install prompt ready');
            });
        </script>
    </body>
    </html>
    '''

@app.route('/static/<path:filename>')
def static_files(filename):
    from flask import send_from_directory
    return send_from_directory('static', filename)

# Create self-signed certificate
import os
import subprocess

cert_file = 'cert.pem'
key_file = 'key.pem'

if not os.path.exists(cert_file):
    print('Creating self-signed certificate...')
    subprocess.run(['openssl', 'req', '-x509', '-newkey', 'rsa:4096', '-keyout', key_file, '-out', cert_file, '-days', '365', '-nodes', '-subj', '/C=US/ST=State/L=City/O=Organization/CN=localhost'], check=False)

# Run with HTTPS
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(cert_file, key_file)
app.run(host='0.0.0.0', port=8443, ssl_context=context, debug=True)
"

:: Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ========================================
    echo   EventApp stopped with an error
    echo ========================================
    echo.
    pause
)
