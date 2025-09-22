# 🚀 PythonAnywhere Deployment Guide for EventApp

## 📋 Your Specific Setup

Based on your WSGI file, here's the exact configuration for your PythonAnywhere account:

**Username:** `rsvp13`  
**Project Path:** `/home/rsvp13/app.course.rsvp`  
**Repository:** `https://github.com/gaxiangchong/app.course.rsvp.git`

---

## 🔧 Step 1: Clone Your Repository

1. **Open a Bash console** on PythonAnywhere
2. **Navigate to your home directory:**
   ```bash
   cd /home/rsvp13
   ```
3. **Clone your repository:**
   ```bash
   git clone https://github.com/gaxiangchong/app.course.rsvp.git
   ```
4. **Navigate to the project:**
   ```bash
   cd app.course.rsvp
   ```

---

## 🐍 Step 2: Set Up Virtual Environment

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## ⚙️ Step 3: Configure Web App

### 3.1 Update WSGI Configuration
1. Go to **Web** tab in PythonAnywhere
2. Click on your web app
3. Click **WSGI configuration file**
4. **Replace the entire content** with:

```python
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
```

### 3.2 Configure Static Files
In the **Web** tab, set these static file mappings:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/rsvp13/app.course.rsvp/static/` |
| `/static/images/` | `/home/rsvp13/app.course.rsvp/static/images/` |

### 3.3 Set Working Directory
Set the working directory to: `/home/rsvp13/app.course.rsvp`

---

## 🔐 Step 4: Environment Configuration

### 4.1 Create Production Environment File
```bash
# In PythonAnywhere Bash console
cd /home/rsvp13/app.course.rsvp
nano .env
```

Add the following content:
```env
SECRET_KEY=your-very-secure-secret-key-here
FLASK_ENV=production
DATABASE_URL=sqlite:///eventapp.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
APP_NAME=EventApp
ADMIN_EMAIL=admin@yourapp.com
```

### 4.2 Generate Secret Key
```bash
# In PythonAnywhere Bash console
python3.11 -c "import secrets; print(secrets.token_hex(32))"
```

---

## 🚀 Step 5: Deploy and Test

### 5.1 Initial Deployment
```bash
# In PythonAnywhere Bash console
cd /home/rsvp13/app.course.rsvp
source venv/bin/activate

# Create database tables
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# Set up admin user
python setup_admin.py
```

### 5.2 Reload Web App
1. Go to **Web** tab in PythonAnywhere
2. Click **Reload** button
3. Visit your website: `http://rsvp13.pythonanywhere.com`

---

## 🔄 Step 6: Update Deployment Workflow

### 6.1 Create Deployment Script
```bash
# In PythonAnywhere Bash console
cd /home/rsvp13/app.course.rsvp
nano deploy.sh
```

Add this content:
```bash
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
echo "🌐 Your app should be available at http://rsvp13.pythonanywhere.com"
```

### 6.2 Make Script Executable
```bash
chmod +x deploy.sh
```

---

## 🔄 Step 7: Future Updates

### 7.1 Local Development Workflow
```bash
# 1. Make changes to your code locally
# 2. Test locally
python app.py

# 3. Commit changes
git add .
git commit -m "Add new feature"
git push origin main

# 4. Deploy to PythonAnywhere
# SSH into PythonAnywhere and run:
cd /home/rsvp13/app.course.rsvp
./deploy.sh
```

### 7.2 Quick Update Commands
```bash
# On PythonAnywhere:
cd /home/rsvp13/app.course.rsvp
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

---

## 🆘 Troubleshooting

### Common Issues:

1. **Import Errors**: Check that the project path in WSGI is correct
2. **Static Files Not Loading**: Verify static file mappings in Web tab
3. **Database Issues**: Ensure database file has proper permissions
4. **Environment Variables**: Check `.env` file exists and is readable

### Debug Commands:
```bash
# Check PythonAnywhere logs
tail -f /var/log/rsvp13.pythonanywhere.com.error.log

# Test Flask app locally on PythonAnywhere
cd /home/rsvp13/app.course.rsvp
source venv/bin/activate
python app.py
```

### Check File Permissions:
```bash
# Make sure files are readable
chmod -R 755 /home/rsvp13/app.course.rsvp
```

---

## 📝 Summary

Your EventApp will be available at: **http://rsvp13.pythonanywhere.com**

**Key Paths:**
- Project: `/home/rsvp13/app.course.rsvp`
- WSGI: Update to point to your project
- Static Files: Map to your static directory
- Environment: Create `.env` file with your settings

**Update Process:**
1. Push changes to GitHub
2. SSH into PythonAnywhere
3. Run `./deploy.sh`
4. Reload web app

---

## 🎉 Ready to Deploy!

Your EventApp is now ready for deployment on PythonAnywhere! Follow these steps and you'll have your professional event management app live on the web! 🚀
