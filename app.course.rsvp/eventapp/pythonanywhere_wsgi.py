# PythonAnywhere WSGI Configuration for EventApp
# Copy this content to your PythonAnywhere WSGI configuration file

import sys
import os

# Add your project directory to the Python path
project_home = '/home/rsvp13/app.course.rsvp/eventapp'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment variables for production
os.environ['FLASK_ENV'] = 'production'

# Import your Flask app but need to call it "application" for WSGI to work
from app import app as application  # noqa

if __name__ == "__main__":
    application.run()
