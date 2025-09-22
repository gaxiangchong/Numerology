#!/usr/bin/env python3
"""
Working PWA EventApp - Fixed version that handles existing database
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
import os
from datetime import datetime

# Create Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eventapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Simple User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    """Home page with PWA features"""
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        
        <!-- PWA Meta Tags -->
        <meta name="application-name" content="EventApp PWA">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="apple-mobile-web-app-title" content="EventApp">
        <meta name="description" content="Event management PWA application">
        <meta name="format-detection" content="telephone=no">
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="theme-color" content="#007bff">
        
        <!-- PWA Manifest -->
        <link rel="manifest" href="/manifest.json">
        
        <!-- Apple Touch Icons -->
        <link rel="apple-touch-icon" href="/static/images/pwa/icon-152x152.png">
        
        <!-- Favicon -->
        <link rel="icon" type="image/png" sizes="32x32" href="/static/images/pwa/icon-32x32.png">
        
        <title>EventApp PWA</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                color: white;
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .header {
                text-align: center;
                margin-bottom: 40px;
            }
            
            .header h1 {
                font-size: 3rem;
                margin-bottom: 10px;
                background: linear-gradient(135deg, #007bff, #00d4ff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .header p {
                font-size: 1.2rem;
                color: #b0b0b0;
            }
            
            .pwa-status {
                background: rgba(0, 123, 255, 0.1);
                border: 1px solid rgba(0, 123, 255, 0.3);
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 30px;
                text-align: center;
            }
            
            .pwa-status h2 {
                color: #00d4ff;
                margin-bottom: 10px;
            }
            
            .install-btn {
                background: linear-gradient(135deg, #007bff, #00d4ff);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                margin: 10px;
                transition: all 0.3s ease;
                display: none;
            }
            
            .install-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
            }
            
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            
            .feature-card {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 20px;
                text-align: center;
            }
            
            .feature-card h3 {
                color: #00d4ff;
                margin-bottom: 10px;
            }
            
            .nav-buttons {
                display: flex;
                gap: 10px;
                justify-content: center;
                margin-top: 20px;
            }
            
            .btn {
                background: rgba(0, 123, 255, 0.2);
                color: #00d4ff;
                border: 1px solid rgba(0, 123, 255, 0.3);
                padding: 10px 20px;
                border-radius: 6px;
                text-decoration: none;
                transition: all 0.3s ease;
            }
            
            .btn:hover {
                background: rgba(0, 123, 255, 0.3);
                transform: translateY(-1px);
            }
            
            .status-message {
                position: fixed;
                top: 20px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(0, 123, 255, 0.9);
                color: white;
                padding: 10px 20px;
                border-radius: 6px;
                z-index: 1000;
                display: none;
            }
            
            @media (max-width: 768px) {
                .header h1 {
                    font-size: 2rem;
                }
                
                .features {
                    grid-template-columns: 1fr;
                }
                
                .nav-buttons {
                    flex-direction: column;
                    align-items: center;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎉 EventApp PWA</h1>
                <p>Progressive Web App - Install on your device!</p>
            </div>
            
            <div class="pwa-status">
                <h2>📱 PWA Ready!</h2>
                <p>This app can be installed on your Android device</p>
                <button id="installBtn" class="install-btn">
                    📱 Install App
                </button>
                <p id="pwaStatus">Checking PWA support...</p>
            </div>
            
            <div class="features">
                <div class="feature-card">
                    <h3>🚀 Offline Support</h3>
                    <p>Works without internet connection</p>
                </div>
                <div class="feature-card">
                    <h3>📱 Native Feel</h3>
                    <p>Full-screen app experience</p>
                </div>
                <div class="feature-card">
                    <h3>🔄 Auto Updates</h3>
                    <p>Updates automatically in background</p>
                </div>
            </div>
            
            <div class="nav-buttons">
                <a href="/login" class="btn">🔐 Login</a>
                <a href="/register" class="btn">📝 Register</a>
                <a href="/test" class="btn">🧪 Test API</a>
            </div>
        </div>
        
        <div id="statusMessage" class="status-message"></div>
        
        <script>
            // PWA Install functionality
            let deferredPrompt;
            const installBtn = document.getElementById('installBtn');
            const pwaStatus = document.getElementById('pwaStatus');
            const statusMessage = document.getElementById('statusMessage');
            
            // Check PWA support
            if ('serviceWorker' in navigator) {
                pwaStatus.textContent = '✅ PWA supported';
                pwaStatus.style.color = '#28a745';
            } else {
                pwaStatus.textContent = '❌ PWA not supported';
                pwaStatus.style.color = '#dc3545';
            }
            
            // Handle install prompt
            window.addEventListener('beforeinstallprompt', (e) => {
                console.log('PWA install prompt triggered');
                e.preventDefault();
                deferredPrompt = e;
                installBtn.style.display = 'inline-block';
                pwaStatus.textContent = '✅ Ready to install!';
                pwaStatus.style.color = '#28a745';
            });
            
            // Handle install button click
            installBtn.addEventListener('click', async () => {
                if (deferredPrompt) {
                    deferredPrompt.prompt();
                    const { outcome } = await deferredPrompt.userChoice;
                    console.log(`PWA install ${outcome}`);
                    if (outcome === 'accepted') {
                        showStatusMessage('App installed successfully!');
                    }
                    deferredPrompt = null;
                    installBtn.style.display = 'none';
                }
            });
            
            // Handle app installed
            window.addEventListener('appinstalled', () => {
                console.log('PWA was installed');
                showStatusMessage('App installed successfully!');
                installBtn.style.display = 'none';
            });
            
            // Register service worker
            if ('serviceWorker' in navigator) {
                navigator.serviceWorker.register('/sw.js')
                    .then((registration) => {
                        console.log('Service Worker registered:', registration);
                    })
                    .catch((error) => {
                        console.log('Service Worker registration failed:', error);
                    });
            }
            
            // Handle online/offline status
            window.addEventListener('online', () => {
                showStatusMessage('You are back online!');
            });
            
            window.addEventListener('offline', () => {
                showStatusMessage('You are offline. App still works!');
            });
            
            function showStatusMessage(message) {
                statusMessage.textContent = message;
                statusMessage.style.display = 'block';
                setTimeout(() => {
                    statusMessage.style.display = 'none';
                }, 3000);
            }
            
            // Check if app is already installed
            if (window.matchMedia('(display-mode: standalone)').matches) {
                pwaStatus.textContent = '✅ App is installed and running!';
                pwaStatus.style.color = '#28a745';
                installBtn.style.display = 'none';
            }
        </script>
    </body>
    </html>
    '''

@app.route('/manifest.json')
def manifest():
    """Serve PWA manifest file"""
    return send_from_directory('static', 'manifest.json', mimetype='application/json')

@app.route('/sw.js')
def service_worker():
    """Serve service worker file"""
    return send_from_directory('static', 'sw.js', mimetype='application/javascript')

@app.route('/test')
def test():
    """Test route"""
    return jsonify({
        'status': 'success',
        'message': 'EventApp PWA is working!',
        'pwa_ready': True,
        'android_urls': {
            'real_device': 'http://192.168.68.116:3000',
            'emulator': 'http://10.0.2.2:3000'
        }
    })

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Simple login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return jsonify({'status': 'success', 'message': 'Login successful'})
        else:
            return jsonify({'status': 'error', 'message': 'Invalid credentials'})
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>EventApp Login</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #1a1a1a; color: white; }
            .container { max-width: 400px; margin: 0 auto; }
            .form-group { margin-bottom: 20px; }
            .form-control { width: 100%; padding: 10px; border: 1px solid #333; border-radius: 5px; background: #2d2d2d; color: white; }
            .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; width: 100%; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>EventApp Login</h1>
            <form method="POST">
                <div class="form-group">
                    <input type="text" name="username" placeholder="Username" class="form-control" required>
                </div>
                <div class="form-group">
                    <input type="password" name="password" placeholder="Password" class="form-control" required>
                </div>
                <button type="submit" class="btn">Login</button>
            </form>
            <p><a href="/">← Back to Home</a></p>
        </div>
    </body>
    </html>
    '''

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Simple registration page"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            return jsonify({'status': 'error', 'message': 'Username already exists'})
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'status': 'success', 'message': 'Registration successful'})
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>EventApp Register</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #1a1a1a; color: white; }
            .container { max-width: 400px; margin: 0 auto; }
            .form-group { margin-bottom: 20px; }
            .form-control { width: 100%; padding: 10px; border: 1px solid #333; border-radius: 5px; background: #2d2d2d; color: white; }
            .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; width: 100%; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>EventApp Register</h1>
            <form method="POST">
                <div class="form-group">
                    <input type="text" name="username" placeholder="Username" class="form-control" required>
                </div>
                <div class="form-group">
                    <input type="email" name="email" placeholder="Email" class="form-control" required>
                </div>
                <div class="form-group">
                    <input type="password" name="password" placeholder="Password" class="form-control" required>
                </div>
                <button type="submit" class="btn">Register</button>
            </form>
            <p><a href="/">← Back to Home</a></p>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    print("=" * 60)
    print("  EventApp PWA - Fixed Version")
    print("=" * 60)
    print()
    print("Your IP address: 192.168.68.116")
    print()
    print("Android access URLs:")
    print("- Real device: http://192.168.68.116:3000")
    print("- Emulator: http://10.0.2.2:3000")
    print()
    print("Starting EventApp on port 3000...")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    # Create database tables (only User table, no Event table to avoid conflicts)
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database initialized")
        except Exception as e:
            print(f"⚠️ Database warning: {e}")
            print("Continuing with existing database...")
    
    # Run the app
    app.run(host='0.0.0.0', debug=True, port=3000)
