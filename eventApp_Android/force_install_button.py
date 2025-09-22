#!/usr/bin/env python3
"""
EventApp with forced install button
"""

from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>EventApp - Force Install</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="theme-color" content="#007bff">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <link rel="manifest" href="/static/manifest.json">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #1a1a1a; color: white; }
            .container { max-width: 600px; margin: 0 auto; }
            .install-btn { background: #28a745; color: white; padding: 15px 30px; border: none; border-radius: 8px; font-size: 18px; font-weight: 600; cursor: pointer; margin: 20px 0; display: block; width: 100%; }
            .install-btn:hover { background: #218838; }
            .manual-install { background: #007bff; color: white; padding: 12px 24px; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; margin: 10px 0; display: block; width: 100%; }
            .manual-install:hover { background: #0056b3; }
            .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
            .success { background: rgba(40, 167, 69, 0.2); border: 1px solid #28a745; }
            .warning { background: rgba(255, 193, 7, 0.2); border: 1px solid #ffc107; }
            .info { background: rgba(0, 123, 255, 0.2); border: 1px solid #007bff; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎉 EventApp PWA - Force Install</h1>
            
            <div class="status success">
                <h3>✅ PWA Ready!</h3>
                <p>This app can be installed on your Android device</p>
            </div>
            
            <button id="installBtn" class="install-btn">
                📱 Install App (Automatic)
            </button>
            
            <div class="status warning">
                <h3>⚠️ If Install Button Doesn't Work:</h3>
                <p>Try these manual methods:</p>
            </div>
            
            <button class="manual-install" onclick="showManualInstructions()">
                📋 Show Manual Instructions
            </button>
            
            <button class="manual-install" onclick="openChromeMenu()">
                ⋮ Open Chrome Menu
            </button>
            
            <div id="manualInstructions" style="display: none; margin-top: 20px; padding: 15px; background: rgba(255, 255, 255, 0.05); border-radius: 8px;">
                <h3>📋 Manual Installation Steps:</h3>
                <ol>
                    <li><strong>Chrome Menu Method:</strong>
                        <ul>
                            <li>Tap the three dots menu (⋮) in Chrome</li>
                            <li>Look for "Add to Home screen"</li>
                            <li>Tap "Add to Home screen"</li>
                            <li>Tap "Add" to confirm</li>
                        </ul>
                    </li>
                    <li><strong>Chrome Apps Page:</strong>
                        <ul>
                            <li>Go to: chrome://apps/</li>
                            <li>Look for your app</li>
                            <li>Tap to install</li>
                        </ul>
                    </li>
                    <li><strong>Chrome Flags:</strong>
                        <ul>
                            <li>Go to: chrome://flags/</li>
                            <li>Search for: "PWA"</li>
                            <li>Enable: "PWA install prompt"</li>
                            <li>Restart Chrome</li>
                        </ul>
                    </li>
                </ol>
            </div>
            
            <div id="pwaStatus" class="status info">
                <h3>🔍 PWA Status:</h3>
                <p id="statusText">Checking PWA support...</p>
            </div>
        </div>
        
        <script>
            // PWA Install functionality
            let deferredPrompt;
            const installBtn = document.getElementById('installBtn');
            const statusText = document.getElementById('statusText');
            
            // Check PWA support
            if ('serviceWorker' in navigator) {
                statusText.textContent = '✅ PWA supported - Service Worker available';
            } else {
                statusText.textContent = '❌ PWA not supported - Service Worker not available';
            }
            
            // Handle install prompt
            window.addEventListener('beforeinstallprompt', (e) => {
                console.log('PWA install prompt triggered');
                e.preventDefault();
                deferredPrompt = e;
                installBtn.textContent = '📱 Install App (Ready!)';
                installBtn.style.background = '#28a745';
                statusText.textContent = '✅ Ready to install! Install button should work now.';
            });
            
            // Handle install button click
            installBtn.addEventListener('click', async () => {
                if (deferredPrompt) {
                    deferredPrompt.prompt();
                    const { outcome } = await deferredPrompt.userChoice;
                    console.log(`PWA install ${outcome}`);
                    if (outcome === 'accepted') {
                        statusText.textContent = '🎉 App installed successfully!';
                    } else {
                        statusText.textContent = '❌ Installation cancelled. Try manual method.';
                    }
                    deferredPrompt = null;
                } else {
                    statusText.textContent = '⚠️ Install prompt not available. Try manual method.';
                }
            });
            
            // Handle app installed
            window.addEventListener('appinstalled', () => {
                console.log('PWA was installed');
                statusText.textContent = '🎉 App installed successfully!';
                installBtn.style.display = 'none';
            });
            
            // Register service worker
            if ('serviceWorker' in navigator) {
                navigator.serviceWorker.register('/static/sw.js')
                    .then((registration) => {
                        console.log('Service Worker registered:', registration);
                        statusText.textContent += ' | Service Worker: ✅';
                    })
                    .catch((error) => {
                        console.log('Service Worker registration failed:', error);
                        statusText.textContent += ' | Service Worker: ❌';
                    });
            }
            
            // Manual installation functions
            function showManualInstructions() {
                const instructions = document.getElementById('manualInstructions');
                instructions.style.display = instructions.style.display === 'none' ? 'block' : 'none';
            }
            
            function openChromeMenu() {
                alert('Tap the three dots menu (⋮) in Chrome, then look for "Add to Home screen"');
            }
            
            // Check if app is already installed
            if (window.matchMedia('(display-mode: standalone)').matches) {
                statusText.textContent = '✅ App is already installed and running!';
                installBtn.style.display = 'none';
            }
        </script>
    </body>
    </html>
    '''

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    print("=" * 60)
    print("  EventApp - Force Install Button")
    print("=" * 60)
    print()
    print("Your IP address: 192.168.68.116")
    print()
    print("Android access URLs:")
    print("- Real device: http://192.168.68.116:3000")
    print("- Emulator: http://10.0.2.2:3000")
    print()
    print("Starting EventApp with forced install button...")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    app.run(host='0.0.0.0', debug=True, port=3000)