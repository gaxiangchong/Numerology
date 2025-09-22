@echo off
echo Preparing Numerology PWA for PythonAnywhere deployment...
echo.

echo Step 1: Creating production requirements...
pip freeze > requirements.txt

echo Step 2: Creating WSGI configuration...
echo #!/usr/bin/python3.10 > wsgi.py
echo import sys, os >> wsgi.py
echo path = '/home/yourusername/numerology-app' >> wsgi.py
echo if path not in sys.path: sys.path.append(path) >> wsgi.py
echo os.environ['FLASK_ENV'] = 'production' >> wsgi.py
echo os.environ['FLASK_APP'] = 'mysite/app.py' >> wsgi.py
echo from mysite.app import app as application >> wsgi.py

echo Step 3: Creating production config...
echo import os > config.py
echo class Config: >> config.py
echo     SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here' >> config.py
echo     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///instance/users.db' >> config.py
echo     SQLALCHEMY_TRACK_MODIFICATIONS = False >> config.py

echo.
echo Files created for deployment:
echo - requirements.txt
echo - wsgi.py
echo - config.py
echo.
echo Next steps:
echo 1. Sign up at https://www.pythonanywhere.com/
echo 2. Upload your project files
echo 3. Follow the deployment guide: PYTHONANYWHERE_DEPLOYMENT_GUIDE.md
echo.
pause
