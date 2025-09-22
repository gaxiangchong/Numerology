#!/bin/bash
# Deployment script for PythonAnywhere

echo "🚀 Starting EventApp deployment..."

# Pull latest changes
echo "📥 Pulling latest changes from Git..."
git pull origin main

# Activate virtual environment
echo "🐍 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📦 Installing/updating dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "🗄️ Updating database..."
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# Create placeholder images if they don't exist
echo "🖼️ Checking placeholder images..."
if [ ! -d "static/images/events" ]; then
    echo "Creating placeholder images..."
    python create_placeholder_images.py
fi

echo "✅ Deployment complete!"
echo "🔄 Please reload your web app in PythonAnywhere dashboard"
echo "🌐 Your app should be available at your PythonAnywhere URL"
