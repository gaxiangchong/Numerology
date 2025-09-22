#!/bin/bash
# Update existing PythonAnywhere deployment
# Run this in PythonAnywhere Bash console

echo "🔄 Updating existing EventApp deployment..."

# Navigate to project directory
cd /home/rsvp13/app.course.rsvp/eventapp

# Pull latest changes
echo "📥 Pulling latest changes from GitHub..."
git pull origin main

# Activate virtual environment
echo "🐍 Activating virtual environment..."
source venv/bin/activate

# Update dependencies
echo "📦 Updating dependencies..."
pip install -r requirements.txt

# Update database schema
echo "🗄️ Updating database schema..."
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database updated successfully!')"

echo "✅ Update complete!"
echo ""
echo "🔄 Next step:"
echo "1. Go to PythonAnywhere Web tab"
echo "2. Click 'Reload' button"
echo "3. Visit: http://rsvp13.pythonanywhere.com"
echo ""
echo "🎉 Your EventApp is now updated with the latest changes!"
