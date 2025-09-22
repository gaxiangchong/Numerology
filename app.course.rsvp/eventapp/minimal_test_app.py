#!/usr/bin/env python3
"""
Minimal test app to debug 500 error
"""

import os
from flask import Flask, render_template_string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test-secret-key'

# Simple test route
@app.route('/')
def test():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test App</title>
    </head>
    <body>
        <h1>✅ App is working!</h1>
        <p>If you can see this, the basic Flask app is working.</p>
        <p>Chinese seal test: <img src="/static/images/logos/chinese-seal.png" alt="Test" style="width: 50px; height: 50px;"></p>
    </body>
    </html>
    '''

@app.route('/test-imports')
def test_imports():
    """Test all imports that might be causing issues"""
    try:
        from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify, send_from_directory
        from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
        from flask_sqlalchemy import SQLAlchemy
        from werkzeug.security import check_password_hash, generate_password_hash
        from dotenv import load_dotenv
        import qrcode
        
        # Test conditional Stripe import
        try:
            import stripe
            stripe_status = "✅ Available"
        except ImportError:
            stripe_status = "❌ Not available (expected)"
        
        return f'''
        <h1>Import Test Results</h1>
        <ul>
            <li>Flask: ✅</li>
            <li>Flask-Login: ✅</li>
            <li>Flask-SQLAlchemy: ✅</li>
            <li>Werkzeug: ✅</li>
            <li>python-dotenv: ✅</li>
            <li>qrcode: ✅</li>
            <li>Stripe: {stripe_status}</li>
        </ul>
        '''
    except Exception as e:
        return f'<h1>Import Error</h1><p>Error: {str(e)}</p>'

if __name__ == '__main__':
    print("🧪 Starting minimal test app...")
    print("📝 Test routes:")
    print("   - http://localhost:5000/ (basic test)")
    print("   - http://localhost:5000/test-imports (import test)")
    app.run(debug=True, port=5000)
