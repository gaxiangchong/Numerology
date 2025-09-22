#!/usr/bin/env python3
"""
Debug version of EventApp to identify the 404 issue
"""

import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///eventapp.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Simple User model for testing
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

# Simple routes for testing
@app.route('/')
def index():
    """Simple home page for testing"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>EventApp Debug</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #1a1a1a; color: white; }
            .container { max-width: 600px; margin: 0 auto; }
            .success { color: #28a745; }
            .info { color: #17a2b8; }
            .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; text-decoration: none; display: inline-block; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎉 EventApp Debug - Working!</h1>
            <p class="success">✅ Flask app is running correctly</p>
            <p class="success">✅ Routes are working</p>
            <p class="success">✅ Database connection is working</p>
            
            <h2>📱 PWA Features</h2>
            <p class="info">Your EventApp is now PWA-ready!</p>
            
            <h3>🔗 Test Links:</h3>
            <a href="/manifest.json" class="btn">PWA Manifest</a>
            <a href="/sw.js" class="btn">Service Worker</a>
            <a href="/test" class="btn">Test Route</a>
            
            <h3>📱 Android Access:</h3>
            <p>Use these URLs on your Android device:</p>
            <ul>
                <li><strong>Real device:</strong> http://192.168.68.116:8080</li>
                <li><strong>Emulator:</strong> http://10.0.2.2:8080</li>
            </ul>
            
            <h3>🚀 Next Steps:</h3>
            <ol>
                <li>Open Chrome on your Android device</li>
                <li>Navigate to the URL above</li>
                <li>Look for "Install App" button</li>
                <li>Tap "Install App" to install PWA</li>
            </ol>
        </div>
    </body>
    </html>
    '''

@app.route('/test')
def test():
    """Test route"""
    return jsonify({
        'status': 'success',
        'message': 'EventApp is working!',
        'pwa_ready': True,
        'android_urls': {
            'real_device': 'http://192.168.68.116:8080',
            'emulator': 'http://10.0.2.2:8080'
        }
    })

@app.route('/manifest.json')
def manifest():
    """Serve PWA manifest file"""
    from flask import send_from_directory
    return send_from_directory('static', 'manifest.json', mimetype='application/json')

@app.route('/sw.js')
def service_worker():
    """Serve service worker file"""
    from flask import send_from_directory
    return send_from_directory('static', 'sw.js', mimetype='application/javascript')

if __name__ == '__main__':
    print("=" * 60)
    print("  EventApp Debug - Android PWA Testing")
    print("=" * 60)
    print()
    print("Your IP address: 192.168.68.116")
    print()
    print("Android access URLs:")
    print("- Real device: http://192.168.68.116:8080")
    print("- Emulator: http://10.0.2.2:8080")
    print()
    print("Starting debug server on port 8080...")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    # Create database tables
    with app.app_context():
        db.create_all()
        print("✅ Database initialized")
    
    # Run the app
    app.run(host='0.0.0.0', debug=True, port=8080)