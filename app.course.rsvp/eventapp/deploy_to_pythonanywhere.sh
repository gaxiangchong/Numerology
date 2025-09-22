#!/bin/bash
# PythonAnywhere Deployment Script for EventApp
# Run this script in PythonAnywhere Bash console

echo "🚀 Starting EventApp deployment to PythonAnywhere..."

# Navigate to home directory
cd /home/rsvp13

# Clone or update repository
if [ -d "app.course.rsvp" ]; then
    echo "📥 Updating existing repository..."
    cd app.course.rsvp
    git pull origin main
else
    echo "📥 Cloning repository..."
    git clone https://github.com/gaxiangchong/app.course.rsvp.git
    cd app.course.rsvp
fi

# Navigate to eventapp directory
cd eventapp

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🐍 Creating virtual environment..."
    python3.11 -m venv venv
fi

# Activate virtual environment
echo "🐍 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️ Creating environment configuration..."
    cat > .env << EOF
SECRET_KEY=$(python3.11 -c "import secrets; print(secrets.token_hex(32))")
FLASK_ENV=production
DATABASE_URL=sqlite:///eventapp.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
APP_NAME=EventApp
ADMIN_EMAIL=admin@yourapp.com
EOF
    echo "⚠️  Please edit .env file with your actual email settings!"
fi

# Create database tables
echo "🗄️ Setting up database..."
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database tables created successfully!')"

# Create admin user if it doesn't exist
echo "👤 Setting up admin user..."
python setup_admin.py

echo "✅ Deployment setup complete!"
echo ""
echo "🔧 Next steps:"
echo "1. Edit .env file with your email settings"
echo "2. Configure Web app in PythonAnywhere dashboard:"
echo "   - Source code: /home/rsvp13/app.course.rsvp/eventapp"
echo "   - Working directory: /home/rsvp13/app.course.rsvp/eventapp"
echo "   - WSGI file: Update to point to your app"
echo "3. Set static file mappings:"
echo "   - /static/ → /home/rsvp13/app.course.rsvp/eventapp/static/"
echo "4. Reload your web app"
echo ""
echo "🌐 Your app will be available at: http://rsvp13.pythonanywhere.com"
