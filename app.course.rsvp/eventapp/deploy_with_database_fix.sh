#!/bin/bash
# 🚀 EventApp Deployment Script with Database Fix
# This script deploys your EventApp to PythonAnywhere with the country_code database fix

echo "🚀 Starting EventApp deployment with database fix..."

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: Please run this script from the eventapp directory"
    echo "Usage: cd eventapp && ./deploy_with_database_fix.sh"
    exit 1
fi

# Pull latest changes
echo "📥 Pulling latest changes from Git..."
git pull origin main

# Activate virtual environment
echo "🐍 Activating virtual environment..."
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "📦 Creating virtual environment..."
    python3.11 -m venv venv
    source venv/bin/activate
fi

# Install/update dependencies
echo "📦 Installing/updating dependencies..."
pip install -r requirements.txt

# Run database migrations (including country_code fix)
echo "🗄️ Applying database migrations..."
if [ -f "migrate_country_code.py" ]; then
    python migrate_country_code.py
else
    echo "⚠️  migrate_country_code.py not found, creating database with all tables..."
fi

# Update database schema
echo "🔧 Updating database schema..."
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# Set up admin user if needed
echo "👤 Setting up admin user..."
if [ -f "setup_admin.py" ]; then
    python setup_admin.py
else
    echo "⚠️  setup_admin.py not found, skipping admin setup"
fi

echo "✅ Deployment complete!"
echo ""
echo "🔄 Next steps:"
echo "1. Go to PythonAnywhere Web tab"
echo "2. Click 'Reload' button"
echo "3. Visit: http://rsvp13.pythonanywhere.com"
echo ""
echo "🌐 Your EventApp should now be live!"
