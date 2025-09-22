#!/usr/bin/env python3
"""
Debug version of the main app - gradually add components to find the issue
"""

import os
from flask import Flask, render_template_string

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'debug-secret-key')

# Test basic app
@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Debug App</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .test { margin: 20px 0; padding: 10px; border: 1px solid #ccc; }
            .success { background-color: #d4edda; border-color: #c3e6cb; }
            .error { background-color: #f8d7da; border-color: #f5c6cb; }
        </style>
    </head>
    <body>
        <h1>🔍 Debug App - Step by Step</h1>
        
        <div class="test success">
            <h3>✅ Step 1: Basic Flask App</h3>
            <p>Flask app is running successfully!</p>
        </div>
        
        <div class="test">
            <h3>🧪 Step 2: Test Imports</h3>
            <p><a href="/test-imports">Test All Imports</a></p>
        </div>
        
        <div class="test">
            <h3>🗄️ Step 3: Test Database</h3>
            <p><a href="/test-database">Test Database Connection</a></p>
        </div>
        
        <div class="test">
            <h3>🎨 Step 4: Test Templates</h3>
            <p><a href="/test-templates">Test Template Rendering</a></p>
        </div>
        
        <div class="test">
            <h3>🖼️ Step 5: Test Static Files</h3>
            <p><a href="/test-static">Test Static Files (Logo)</a></p>
        </div>
    </body>
    </html>
    '''

@app.route('/test-imports')
def test_imports():
    """Test all imports"""
    results = []
    
    try:
        from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify, send_from_directory
        results.append("✅ Flask imports")
    except Exception as e:
        results.append(f"❌ Flask imports: {e}")
    
    try:
        from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
        results.append("✅ Flask-Login imports")
    except Exception as e:
        results.append(f"❌ Flask-Login imports: {e}")
    
    try:
        from flask_sqlalchemy import SQLAlchemy
        results.append("✅ Flask-SQLAlchemy imports")
    except Exception as e:
        results.append(f"❌ Flask-SQLAlchemy imports: {e}")
    
    try:
        from werkzeug.security import check_password_hash, generate_password_hash
        results.append("✅ Werkzeug imports")
    except Exception as e:
        results.append(f"❌ Werkzeug imports: {e}")
    
    try:
        from dotenv import load_dotenv
        results.append("✅ python-dotenv imports")
    except Exception as e:
        results.append(f"❌ python-dotenv imports: {e}")
    
    try:
        import qrcode
        results.append("✅ QRCode imports")
    except Exception as e:
        results.append(f"❌ QRCode imports: {e}")
    
    try:
        import stripe
        results.append("✅ Stripe imports (available)")
    except ImportError:
        results.append("✅ Stripe imports (not available - expected)")
    except Exception as e:
        results.append(f"❌ Stripe imports: {e}")
    
    return f'''
    <h1>Import Test Results</h1>
    <ul>
        {''.join([f'<li>{result}</li>' for result in results])}
    </ul>
    <p><a href="/">← Back to Debug Menu</a></p>
    '''

@app.route('/test-database')
def test_database():
    """Test database connection"""
    try:
        from flask_sqlalchemy import SQLAlchemy
        
        # Configure database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db = SQLAlchemy(app)
        
        # Test database connection
        with app.app_context():
            db.create_all()
            result = db.engine.execute("SELECT 1").fetchone()
        
        return '''
        <h1>✅ Database Test Passed</h1>
        <p>Database connection and basic operations are working!</p>
        <p><a href="/">← Back to Debug Menu</a></p>
        '''
    except Exception as e:
        return f'''
        <h1>❌ Database Test Failed</h1>
        <p>Error: {str(e)}</p>
        <p><a href="/">← Back to Debug Menu</a></p>
        '''

@app.route('/test-templates')
def test_templates():
    """Test template rendering"""
    try:
        from flask import render_template
        
        # Test if templates directory exists and is accessible
        template_path = os.path.join(app.root_path, 'templates')
        if os.path.exists(template_path):
            return f'''
            <h1>✅ Templates Test Passed</h1>
            <p>Templates directory exists at: {template_path}</p>
            <p><a href="/">← Back to Debug Menu</a></p>
            '''
        else:
            return f'''
            <h1>❌ Templates Test Failed</h1>
            <p>Templates directory not found at: {template_path}</p>
            <p><a href="/">← Back to Debug Menu</a></p>
            '''
    except Exception as e:
        return f'''
        <h1>❌ Templates Test Failed</h1>
        <p>Error: {str(e)}</p>
        <p><a href="/">← Back to Debug Menu</a></p>
        '''

@app.route('/test-static')
def test_static():
    """Test static files"""
    try:
        static_path = os.path.join(app.root_path, 'static', 'images', 'logos')
        logo_path = os.path.join(static_path, 'chinese-seal.png')
        
        if os.path.exists(logo_path):
            return f'''
            <h1>✅ Static Files Test Passed</h1>
            <p>Chinese seal logo found at: {logo_path}</p>
            <p>Logo: <img src="/static/images/logos/chinese-seal.png" alt="Chinese Seal" style="width: 50px; height: 50px;"></p>
            <p><a href="/">← Back to Debug Menu</a></p>
            '''
        else:
            return f'''
            <h1>⚠️ Static Files Test - Logo Not Found</h1>
            <p>Logo not found at: {logo_path}</p>
            <p>Static directory exists: {os.path.exists(static_path)}</p>
            <p><a href="/">← Back to Debug Menu</a></p>
            '''
    except Exception as e:
        return f'''
        <h1>❌ Static Files Test Failed</h1>
        <p>Error: {str(e)}</p>
        <p><a href="/">← Back to Debug Menu</a></p>
        '''

if __name__ == '__main__':
    print("🔍 Starting debug app...")
    print("📝 Debug routes:")
    print("   - http://localhost:5001/ (debug menu)")
    print("   - http://localhost:5001/test-imports")
    print("   - http://localhost:5001/test-database")
    print("   - http://localhost:5001/test-templates")
    print("   - http://localhost:5001/test-static")
    app.run(debug=True, port=5001)
