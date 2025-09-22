# This file contains the WSGI configuration required to serve up your
# EventApp web application at http://<your-username>.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.

import sys
import os

# Add your project directory to the sys.path
project_home = '/home/rsvp13/app.course.rsvp'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment variables for production
os.environ['FLASK_ENV'] = 'production'

# Import your Flask app but need to call it "application" for WSGI to work
from app import app as application  # noqa

# Optional: Set additional environment variables if needed
# os.environ['SECRET_KEY'] = 'your-secret-key-here'
# os.environ['DATABASE_URL'] = 'sqlite:///eventapp.db'
