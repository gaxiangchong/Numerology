#!/bin/bash
# Deploy Latest Updates to PythonAnywhere
# This script updates your existing PythonAnywhere deployment with the latest changes

echo "🚀 Deploying Latest EventApp Updates to PythonAnywhere..."
echo "=================================================="

# Navigate to project directory
echo "📁 Navigating to project directory..."
cd /home/rsvp13/app.course.rsvp/eventapp

# Pull latest changes from GitHub
echo "📥 Pulling latest changes from GitHub..."
git pull origin main

# Activate virtual environment
echo "🐍 Activating virtual environment..."
source venv/bin/activate

# Update dependencies
echo "📦 Updating dependencies..."
pip install -r requirements.txt

# Update .env file with production settings
echo "⚙️ Updating environment configuration for production..."
cat > .env << EOF
# EventApp Environment Configuration
# Generated for SendGrid email service

# Flask Configuration
SECRET_KEY=$(python3.11 -c "import secrets; print(secrets.token_hex(32))")
FLASK_ENV=production
DATABASE_URL=sqlite:///eventapp.db

# Flask URL Configuration (for email verification)
SERVER_NAME=rsvp13.pythonanywhere.com
APPLICATION_ROOT=/
PREFERRED_URL_SCHEME=https

# Email Configuration (SendGrid)
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=apikey
MAIL_PASSWORD=YOUR_SENDGRID_API_KEY_HERE

# App Configuration
APP_NAME=EventApp
ADMIN_EMAIL=noblequest.edu@outlook.com
EOF

# Update database schema
echo "🗄️ Updating database schema..."
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database updated successfully!')"

# Set proper file permissions
echo "🔐 Setting file permissions..."
chmod -R 755 /home/rsvp13/app.course.rsvp/eventapp

echo ""
echo "✅ Deployment update complete!"
echo "=================================================="
echo ""
echo "🔄 Next steps:"
echo "1. Go to PythonAnywhere Web tab"
echo "2. Click 'Reload' button"
echo "3. Visit: https://rsvp13.pythonanywhere.com"
echo ""
echo "🎉 Your EventApp is now updated with:"
echo "   ✅ Email verification system"
echo "   ✅ Purple gradient backgrounds"
echo "   ✅ Red-to-purple logo gradient"
echo "   ✅ Resend verification with timer"
echo "   ✅ SendGrid email configuration"
echo ""
echo "🌐 Your app: https://rsvp13.pythonanywhere.com"
