#!/usr/bin/env python3
"""
Working PWA EventApp - Combines simple functionality with full PWA features
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
import os

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

# Simple Event model
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200))
    capacity = db.Column(db.Integer, default=100)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Routes
@app.route('/')
def index():
    """Home page with PWA features"""
    events = Event.query.order_by(Event.date.asc()).limit(6).all()
    return render_template('index.html', events=events)

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
    print("  EventApp PWA - Working Version")
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
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@example.com', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created (admin/admin123)")
        
        # Create sample event if not exists
        if not Event.query.first():
            event = Event(
                name='Sample Event',
                description='This is a sample event for testing',
                date=db.func.current_timestamp(),
                location='Sample Location',
                capacity=50,
                creator_id=1
            )
            db.session.add(event)
            db.session.commit()
            print("✅ Sample event created")
        
        print("✅ Database initialized")
    
    # Run the app
    app.run(host='0.0.0.0', debug=True, port=3000)
