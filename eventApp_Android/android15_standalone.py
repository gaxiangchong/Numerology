#!/usr/bin/env python3
"""
EventApp - Android 15 Compatible Standalone PWA
Optimized for Android 15's stricter PWA requirements
"""

from flask import Flask, send_from_directory, render_template_string
import os

app = Flask(__name__)

# Enhanced PWA Manifest for Android 15
PWA_MANIFEST = {
    "name": "EventApp - Standalone",
    "short_name": "EventApp",
    "description": "A comprehensive event management system",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#1a1a1a",
    "theme_color": "#007bff",
    "orientation": "portrait",
    "scope": "/",
    "categories": ["productivity", "business"],
    "lang": "en",
    "dir": "ltr",
    "prefer_related_applications": False,
    "icons": [
        {
            "src": "/static/images/pwa/icon-72x72.png",
            "sizes": "72x72",
            "type": "image/png",
            "purpose": "any"
        },
        {
            "src": "/static/images/pwa/icon-96x96.png",
            "sizes": "96x96",
            "type": "image/png",
            "purpose": "any"
        },
        {
            "src": "/static/images/pwa/icon-128x128.png",
            "sizes": "128x128",
            "type": "image/png",
            "purpose": "any"
        },
        {
            "src": "/static/images/pwa/icon-144x144.png",
            "sizes": "144x144",
            "type": "image/png",
            "purpose": "any"
        },
        {
            "src": "/static/images/pwa/icon-152x152.png",
            "sizes": "152x152",
            "type": "image/png",
            "purpose": "any"
        },
        {
            "src": "/static/images/pwa/icon-192x192.png",
            "sizes": "192x192",
            "type": "image/png",
            "purpose": "any maskable"
        },
        {
            "src": "/static/images/pwa/icon-384x384.png",
            "sizes": "384x384",
            "type": "image/png",
            "purpose": "any"
        },
        {
            "src": "/static/images/pwa/icon-512x512.png",
            "sizes": "512x512",
            "type": "image/png",
            "purpose": "any maskable"
        }
    ],
    "screenshots": [
        {
            "src": "/static/images/pwa/screenshot1.png",
            "sizes": "1280x720",
            "type": "image/png",
            "form_factor": "wide"
        }
    ]
}

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>EventApp - Android 15 Standalone</title>
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no, viewport-fit=cover">
        <meta name="theme-color" content="#007bff">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="apple-mobile-web-app-title" content="EventApp">
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="application-name" content="EventApp">
        <meta name="msapplication-TileColor" content="#007bff">
        <meta name="msapplication-config" content="/browserconfig.xml">
        <link rel="manifest" href="/manifest.json">
        <link rel="apple-touch-icon" href="/static/images/pwa/icon-192x192.png">
        <link rel="icon" type="image/png" sizes="192x192" href="/static/images/pwa/icon-192x192.png">
        <link rel="icon" type="image/png" sizes="512x512" href="/static/images/pwa/icon-512x512.png">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                color: white;
                height: 100vh;
                overflow: hidden;
                display: flex;
                flex-direction: column;
                -webkit-user-select: none;
                user-select: none;
            }
            .app-header {
                background: rgba(0, 123, 255, 0.95);
                padding: 20px;
                text-align: center;
                box-shadow: 0 2px 20px rgba(0,0,0,0.3);
                backdrop-filter: blur(10px);
            }
            .app-title {
                font-size: 28px;
                font-weight: 700;
                margin: 0;
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            }
            .app-subtitle {
                font-size: 16px;
                opacity: 0.9;
                margin: 8px 0 0 0;
                font-weight: 400;
            }
            .app-content {
                flex: 1;
                padding: 30px 20px;
                overflow-y: auto;
                text-align: center;
            }
            .status-card {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                padding: 30px;
                margin: 25px 0;
                backdrop-filter: blur(15px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            }
            .install-btn {
                background: linear-gradient(45deg, #28a745, #20c997);
                color: white;
                padding: 20px 40px;
                border: none;
                border-radius: 30px;
                font-size: 20px;
                font-weight: 700;
                cursor: pointer;
                margin: 25px 0;
                display: block;
                width: 100%;
                box-shadow: 0 6px 20px rgba(40, 167, 69, 0.4);
                transition: all 0.3s ease;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            .install-btn:hover {
                transform: translateY(-3px);
                box-shadow: 0 8px 25px rgba(40, 167, 69, 0.5);
            }
            .manual-btn {
                background: rgba(0, 123, 255, 0.9);
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 25px;
                font-size: 18px;
                font-weight: 600;
                cursor: pointer;
                margin: 15px 0;
                display: block;
                width: 100%;
                transition: all 0.3s ease;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            .manual-btn:hover {
                background: rgba(0, 123, 255, 1);
                transform: translateY(-2px);
            }
            .status-text {
                font-size: 18px;
                margin: 20px 0;
                padding: 20px;
                background: rgba(0, 0, 0, 0.4);
                border-radius: 15px;
                border-left: 5px solid #007bff;
                text-align: left;
            }
            .success { border-left-color: #28a745; }
            .warning { border-left-color: #ffc107; }
            .error { border-left-color: #dc3545; }
            .instructions {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 15px;
                padding: 25px;
                margin: 25px 0;
                text-align: left;
                display: none;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            .instructions h3 {
                color: #007bff;
                margin-bottom: 20px;
                font-size: 20px;
            }
            .instructions ol {
                padding-left: 25px;
            }
            .instructions li {
                margin: 15px 0;
                line-height: 1.6;
                font-size: 16px;
            }
            .instructions ul {
                margin: 10px 0;
                padding-left: 20px;
            }
            .app-footer {
                background: rgba(0, 0, 0, 0.6);
                padding: 20px;
                text-align: center;
                font-size: 16px;
                opacity: 0.8;
                backdrop-filter: blur(10px);
            }
            .android15-note {
                background: rgba(255, 193, 7, 0.2);
                border: 1px solid #ffc107;
                border-radius: 10px;
                padding: 15px;
                margin: 20px 0;
                text-align: left;
            }
            .android15-note h4 {
                color: #ffc107;
                margin-bottom: 10px;
            }
        </style>
    </head>
    <body>
        <div class="app-header">
            <h1 class="app-title">📱 EventApp</h1>
            <p class="app-subtitle">Android 15 Compatible Standalone App</p>
        </div>
        
        <div class="app-content">
            <div class="status-card">
                <h2>🎉 Android 15 Standalone App</h2>
                <p>This PWA is optimized for Android 15's stricter requirements and will run as a true standalone app!</p>
            </div>
            
            <div class="android15-note">
                <h4>📱 Android 15 Note:</h4>
                <p>Android 15 has stricter PWA requirements. The install button may not appear automatically, but the manual installation method will create a true standalone app.</p>
            </div>
            
            <button id="installBtn" class="install-btn">
                📱 Install as Standalone App
            </button>
            
            <div class="status-text" id="pwaStatus">
                Checking Android 15 PWA support...
            </div>
            
            <button class="manual-btn" onclick="showInstructions()">
                📋 Android 15 Installation Guide
            </button>
            
            <div class="instructions" id="instructions">
                <h3>📋 Android 15 Installation Steps:</h3>
                <ol>
                    <li><strong>Chrome Menu Method (Recommended):</strong>
                        <ul>
                            <li>Tap the three dots menu (⋮) in Chrome</li>
                            <li>Look for "Add to Home screen" or "Install app"</li>
                            <li>Tap it and follow the prompts</li>
                            <li>This will create a true standalone app</li>
                        </ul>
                    </li>
                    <li><strong>Chrome Settings Method:</strong>
                        <ul>
                            <li>Go to: chrome://settings/</li>
                            <li>Tap "Site settings"</li>
                            <li>Find your app in the list</li>
                            <li>Look for "Install" option</li>
                        </ul>
                    </li>
                    <li><strong>Chrome Flags (if needed):</strong>
                        <ul>
                            <li>Go to: chrome://flags/</li>
                            <li>Search for: "PWA"</li>
                            <li>Enable: "PWA install prompt"</li>
                            <li>Enable: "Desktop PWA install"</li>
                            <li>Restart Chrome</li>
                        </ul>
                    </li>
                    <li><strong>After Installation:</strong>
                        <ul>
                            <li>Tap the app icon on your home screen</li>
                            <li>It will open as a standalone app (no browser UI)</li>
                            <li>Looks and feels like a native Android app</li>
                        </ul>
                    </li>
                </ol>
            </div>
        </div>
        
        <div class="app-footer">
            <p>EventApp - Android 15 Compatible Standalone PWA</p>
        </div>
        
        <script>
            // PWA Install functionality for Android 15
            let deferredPrompt;
            const installBtn = document.getElementById('installBtn');
            const pwaStatus = document.getElementById('pwaStatus');
            
            // Check PWA support
            if ('serviceWorker' in navigator) {
                pwaStatus.textContent = '✅ PWA supported - Ready for Android 15 standalone installation';
                pwaStatus.className = 'status-text success';
            } else {
                pwaStatus.textContent = '❌ PWA not supported on this device';
                pwaStatus.className = 'status-text error';
            }
            
            // Handle install prompt
            window.addEventListener('beforeinstallprompt', (e) => {
                console.log('PWA install prompt triggered');
                e.preventDefault();
                deferredPrompt = e;
                installBtn.textContent = '📱 Install as Standalone App (Ready!)';
                installBtn.style.background = 'linear-gradient(45deg, #28a745, #20c997)';
                pwaStatus.textContent = '✅ Ready to install as standalone app on Android 15!';
                pwaStatus.className = 'status-text success';
            });
            
            // Handle install button click
            installBtn.addEventListener('click', async () => {
                if (deferredPrompt) {
                    deferredPrompt.prompt();
                    const { outcome } = await deferredPrompt.userChoice;
                    console.log(`PWA install ${outcome}`);
                    if (outcome === 'accepted') {
                        pwaStatus.textContent = '🎉 App installed! Check your home screen for the standalone app.';
                        pwaStatus.className = 'status-text success';
                        installBtn.style.display = 'none';
                    } else {
                        pwaStatus.textContent = '❌ Installation cancelled. Use manual method for Android 15.';
                        pwaStatus.className = 'status-text warning';
                    }
                    deferredPrompt = null;
                } else {
                    pwaStatus.textContent = '⚠️ Install prompt not available on Android 15. Use manual method.';
                    pwaStatus.className = 'status-text warning';
                }
            });
            
            // Handle app installed
            window.addEventListener('appinstalled', () => {
                console.log('PWA was installed');
                pwaStatus.textContent = '🎉 Standalone app installed successfully on Android 15!';
                pwaStatus.className = 'status-text success';
                installBtn.style.display = 'none';
            });
            
            // Register service worker
            if ('serviceWorker' in navigator) {
                navigator.serviceWorker.register('/static/sw.js')
                    .then((registration) => {
                        console.log('Service Worker registered:', registration);
                        pwaStatus.textContent += ' | Service Worker: ✅';
                    })
                    .catch((error) => {
                        console.log('Service Worker registration failed:', error);
                        pwaStatus.textContent += ' | Service Worker: ❌';
                    });
            }
            
            // Check if app is already installed
            if (window.matchMedia('(display-mode: standalone)').matches) {
                pwaStatus.textContent = '✅ App is already installed and running in standalone mode on Android 15!';
                pwaStatus.className = 'status-text success';
                installBtn.style.display = 'none';
            }
            
            // Manual instructions
            function showInstructions() {
                const instructions = document.getElementById('instructions');
                instructions.style.display = instructions.style.display === 'none' ? 'block' : 'none';
            }
            
            // Android 15 specific checks
            if (navigator.userAgent.includes('Android')) {
                pwaStatus.textContent += ' | Android detected';
                if (navigator.userAgent.includes('Android 15')) {
                    pwaStatus.textContent += ' | Android 15 detected - Use manual installation';
                    pwaStatus.className = 'status-text warning';
                }
            }
        </script>
    </body>
    </html>
    ''')

@app.route('/manifest.json')
def manifest():
    return PWA_MANIFEST

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    print("=" * 60)
    print("  EventApp - Android 15 Compatible Standalone PWA")
    print("=" * 60)
    print()
    print("Your IP address: 192.168.68.116")
    print()
    print("Android access URLs:")
    print("- Real device: http://192.168.68.116:3000")
    print("- Emulator: http://10.0.2.2:3000")
    print()
    print("Features:")
    print("- Optimized for Android 15")
    print("- Runs as standalone app (no browser UI)")
    print("- Installs from home screen")
    print("- Works offline")
    print("- Looks like native app")
    print()
    print("Starting EventApp for Android 15...")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    app.run(host='0.0.0.0', debug=True, port=3000)

