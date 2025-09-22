# Debug WSGI file for PythonAnywhere
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/rsvp13/app.course.rsvp'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment variables for production
os.environ['FLASK_ENV'] = 'production'

# Import the debug Flask app
from debug_app import app as application

if __name__ == "__main__":
    application.run()
