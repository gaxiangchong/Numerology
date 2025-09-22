#!/usr/bin/python3.10
import sys
import os

# Add your project directory to the Python path
path = '/home/yourusername/numerology-app'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['FLASK_ENV'] = 'production'
os.environ['FLASK_APP'] = 'mysite/app.py'

# Import your Flask app
from mysite.app import app as application

if __name__ == "__main__":
    application.run()
