#!/bin/bash
# PythonAnywhere Setup Script for Numerology PWA

echo "Setting up Numerology PWA on PythonAnywhere..."

# Create virtual environment
echo "Creating virtual environment..."
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Set up database
echo "Setting up database..."
cd mysite
python create_db.py
python manage.py db upgrade

# Create instance directory
echo "Creating instance directory..."
mkdir -p instance

# Set permissions
echo "Setting permissions..."
chmod 755 instance
chmod 644 instance/users.db

echo "Setup complete!"
echo "Next steps:"
echo "1. Configure WSGI file in PythonAnywhere dashboard"
echo "2. Set up static files mapping"
echo "3. Add environment variables"
echo "4. Reload your web app"
echo ""
echo "Your app will be available at: https://yourusername.pythonanywhere.com"
