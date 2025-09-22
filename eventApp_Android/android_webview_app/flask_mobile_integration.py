#!/usr/bin/env python3
"""
Flask integration for Android WebView app
Add this to your Flask app to detect mobile/standalone mode
"""

from flask import request, render_template_string

def add_mobile_detection(app):
    """Add mobile detection to Flask app"""
    
    @app.before_request
    def detect_mobile():
        """Detect if request is from mobile/standalone app"""
        user_agent = request.headers.get('User-Agent', '')
        
        # Check if it's from Android WebView
        is_android_webview = 'EventApp-Android' in user_agent
        is_mobile = request.args.get('mobile') == '1'
        is_standalone = request.args.get('standalone') == '1'
        is_fullscreen = request.args.get('fullscreen') == '1'
        
        # Add to request context
        request.is_android_webview = is_android_webview
        request.is_mobile = is_mobile or is_android_webview
        request.is_standalone = is_standalone or is_android_webview
        request.is_fullscreen = is_fullscreen or is_android_webview
        
        # Add mobile-specific headers
        if request.is_mobile:
            request.mobile_viewport = True
            request.hide_browser_ui = True

def add_mobile_css(app):
    """Add mobile-specific CSS"""
    
    mobile_css = """
    <style>
    /* Mobile/Standalone specific styles */
    @media (max-width: 768px) {
        body {
            margin: 0;
            padding: 0;
            overflow-x: hidden;
        }
        
        .container {
            width: 100% !important;
            max-width: 100% !important;
            margin: 0 !important;
            padding: 10px !important;
        }
        
        .navbar {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            background: #fff;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .main-content {
            margin-top: 60px;
            padding: 10px;
        }
        
        .btn {
            width: 100%;
            margin: 5px 0;
            padding: 12px;
            font-size: 16px;
        }
        
        .form-control {
            width: 100%;
            padding: 12px;
            font-size: 16px;
            margin: 5px 0;
        }
        
        .card {
            margin: 10px 0;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .table-responsive {
            overflow-x: auto;
        }
        
        .table {
            font-size: 14px;
        }
        
        .table th, .table td {
            padding: 8px;
        }
    }
    
    /* Standalone app specific styles */
    .standalone-app {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        overflow: hidden;
    }
    
    .standalone-app .navbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
    }
    
    .standalone-app .main-content {
        position: absolute;
        top: 60px;
        left: 0;
        right: 0;
        bottom: 0;
        overflow-y: auto;
        padding: 10px;
    }
    
    /* Hide browser-specific elements in standalone mode */
    .standalone-app .browser-only {
        display: none !important;
    }
    
    /* Mobile navigation */
    .mobile-nav {
        display: none;
    }
    
    @media (max-width: 768px) {
        .mobile-nav {
            display: block;
        }
        
        .desktop-nav {
            display: none;
        }
    }
    </style>
    """
    
    @app.context_processor
    def inject_mobile_css():
        return {'mobile_css': mobile_css}

def add_mobile_js(app):
    """Add mobile-specific JavaScript"""
    
    mobile_js = """
    <script>
    // Mobile/Standalone detection
    function isMobile() {
        return window.innerWidth <= 768 || 
               navigator.userAgent.includes('Mobile') ||
               navigator.userAgent.includes('EventApp-Android');
    }
    
    function isStandalone() {
        return window.navigator.standalone === true ||
               window.matchMedia('(display-mode: standalone)').matches ||
               window.location.search.includes('standalone=1');
    }
    
    // Apply mobile styles
    function applyMobileStyles() {
        if (isMobile() || isStandalone()) {
            document.body.classList.add('mobile-app');
            document.body.classList.add('standalone-app');
            
            // Hide browser-specific elements
            const browserElements = document.querySelectorAll('.browser-only');
            browserElements.forEach(el => el.style.display = 'none');
            
            // Adjust viewport
            document.documentElement.style.overflow = 'hidden';
            document.body.style.overflow = 'hidden';
        }
    }
    
    // Initialize on load
    document.addEventListener('DOMContentLoaded', function() {
        applyMobileStyles();
        
        // Handle orientation change
        window.addEventListener('orientationchange', function() {
            setTimeout(applyMobileStyles, 100);
        });
        
        // Handle resize
        window.addEventListener('resize', function() {
            setTimeout(applyMobileStyles, 100);
        });
    });
    
    // Handle file uploads for mobile
    function handleFileUpload(filePath) {
        console.log('File uploaded:', filePath);
        // Add your file upload logic here
    }
    
    // Handle camera results for mobile
    function handleCameraResult(imagePath) {
        console.log('Camera image:', imagePath);
        // Add your camera logic here
    }
    </script>
    """
    
    @app.context_processor
    def inject_mobile_js():
        return {'mobile_js': mobile_js}

def setup_mobile_flask_app(app):
    """Complete mobile setup for Flask app"""
    
    # Add mobile detection
    add_mobile_detection(app)
    
    # Add mobile CSS
    add_mobile_css(app)
    
    # Add mobile JavaScript
    add_mobile_js(app)
    
    # Add mobile-specific route
    @app.route('/mobile')
    def mobile_home():
        """Mobile-optimized home page"""
        return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>EventApp Mobile</title>
            {{ mobile_css | safe }}
        </head>
        <body>
            <div class="standalone-app">
                <nav class="navbar">
                    <div class="container">
                        <h1>EventApp Mobile</h1>
                    </div>
                </nav>
                <div class="main-content">
                    <div class="container">
                        <h2>Welcome to EventApp Mobile</h2>
                        <p>This is the mobile-optimized version of your Flask app.</p>
                        <a href="/" class="btn btn-primary">Go to Main App</a>
                    </div>
                </div>
            </div>
            {{ mobile_js | safe }}
        </body>
        </html>
        """)

# Example usage:
# from flask import Flask
# app = Flask(__name__)
# setup_mobile_flask_app(app)

