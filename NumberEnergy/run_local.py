#!/usr/bin/env python3
"""
Simple script to run the Flask app locally for development
"""

import os
import sys

# Add the mysite directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mysite'))

# Change to the mysite directory
os.chdir(os.path.join(os.path.dirname(__file__), 'mysite'))

# Import and run the app
from app import app

if __name__ == '__main__':
    print("Starting Flask app locally...")
    print("Open your browser and go to: http://127.0.0.1:5000")
    print("Press Ctrl+C to stop the server")
    app.run(debug=True, host='127.0.0.1', port=5000)
