#!/usr/bin/env python3
"""
WSGI configuration for event.noblequest.com
"""

import sys
import os

# Add the project directory to Python path
project_dir = '/home/rsvp13/app.course.rsvp/eventapp'
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

# Change to the project directory
os.chdir(project_dir)

# Import the Flask application
from app import app as application

# Set environment variables for the new domain
os.environ['SERVER_NAME'] = 'event.noblequest.com'
os.environ['APPLICATION_ROOT'] = '/'

if __name__ == "__main__":
    application.run()
