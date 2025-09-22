#!/usr/bin/env python3
"""
WSGI configuration for redirecting rsvp13.pythonanywhere.com to event.mynoblequest.com
"""

import sys
import os

# Add the project directory to Python path
project_dir = '/home/rsvp13/app.course.rsvp'
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

# Change to the project directory
os.chdir(project_dir)

# Import the redirect application
from redirect_old_domain import app as application

if __name__ == "__main__":
    application.run()
