#!/usr/bin/env python3
"""
WSGI configuration for event.mynoblequest.com
"""

import sys
import os

# Add the project directory to Python path
project_dir = '/home/rsvp13/app.course.rsvp/eventapp'
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

# Change to the project directory
os.chdir(project_dir)

# Set environment variables for the new domain
os.environ['SERVER_NAME'] = 'event.mynoblequest.com'
os.environ['APPLICATION_ROOT'] = '/'

# Import the Flask application
from app import app as application

if __name__ == "__main__":
    application.run()
