# 🚀 Complete Deployment Guide with Database Fix

## 📋 Pre-Deployment Checklist

✅ **Database Issue Fixed**: The `country_code` column has been added to your local database  
✅ **Dependencies Installed**: All required packages are installed  
✅ **Code Ready**: Your app is ready for deployment  

---

## 🎯 Deployment Options

You have **3 deployment options**:

### Option 1: 🚀 **Quick Deploy** (Recommended - 5 minutes)
Use the automated deployment script

### Option 2: 📋 **Manual Deploy** (10 minutes)  
Step-by-step manual deployment

### Option 3: 🔄 **Update Existing** (3 minutes)
If you already have the app deployed

---

## 🚀 Option 1: Quick Deploy (Recommended)

### Step 1: Access PythonAnywhere
1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Log in with your `rsvp13` account
3. Open a **Bash console**

### Step 2: Run Quick Deploy Script
```bash
# Navigate to your home directory
cd /home/rsvp13

# Clone/update your repository
git clone https://github.com/gaxiangchong/app.course.rsvp.git
cd app.course.rsvp/eventapp

# Run the automated deployment
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create database with all tables (including country_code fix)
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# Set up admin user
python setup_admin.py
```

### Step 3: Configure Web App
1. Go to **Web** tab in PythonAnywhere
2. Click **Add a new web app** (or edit existing)
3. Choose **Flask** and **Python 3.11**
4. Set **Source code** to: `/home/rsvp13/app.course.rsvp/eventapp`
5. Set **Working directory** to: `/home/rsvp13/app.course.rsvp/eventapp`

### Step 4: Update WSGI Configuration
Click **WSGI configuration file** and replace with:
```python
import sys
import os

project_home = '/home/rsvp13/app.course.rsvp/eventapp'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

os.environ['FLASK_ENV'] = 'production'
from app import app as application
```

### Step 5: Configure Static Files
In the **Web** tab, add these static file mappings:
- **URL**: `/static/`
- **Directory**: `/home/rsvp13/app.course.rsvp/eventapp/static/`

### Step 6: Create Environment File
```bash
cd /home/rsvp13/app.course.rsvp/eventapp
nano .env
```

Add this content:
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

### Step 7: Reload and Test
1. Click **Reload** button in Web tab
2. Visit: `http://rsvp13.pythonanywhere.com`
3. Login with admin credentials

---

## 📋 Option 2: Manual Deploy (Step-by-Step)

### Step 1: Prepare Your Repository
```bash
# On your local machine, commit the database fix
git add .
git commit -m "Fix database country_code column issue"
git push origin main
```

### Step 2: Deploy to PythonAnywhere
```bash
# In PythonAnywhere Bash console
cd /home/rsvp13

# Clone or update repository
if [ -d "app.course.rsvp" ]; then
    cd app.course.rsvp
    git pull origin main
else
    git clone https://github.com/gaxiangchong/app.course.rsvp.git
    cd app.course.rsvp/eventapp
fi

# Set up virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create database with all tables
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# Run database migrations (including country_code fix)
python migrate_country_code.py

# Set up admin user
python setup_admin.py
```

### Step 3: Configure Web Application
Follow the same WSGI and static file configuration as Option 1.

---

## 🔄 Option 3: Update Existing Deployment

If you already have the app deployed:

### Step 1: Update Code
```bash
# In PythonAnywhere Bash console
cd /home/rsvp13/app.course.rsvp/eventapp
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Apply Database Fix
```bash
# Run the country_code migration
python migrate_country_code.py

# Update database schema
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### Step 3: Reload Application
1. Go to **Web** tab in PythonAnywhere
2. Click **Reload** button

---

## 🛠️ Create Deployment Script

Create a reusable deployment script:

```bash
# In PythonAnywhere Bash console
cd /home/rsvp13/app.course.rsvp/eventapp
nano deploy_with_fix.sh
```

Add this content:
```bash
#!/bin/bash
echo "🚀 Starting EventApp deployment with database fix..."

# Pull latest changes
echo "📥 Pulling latest changes from Git..."
git pull origin main

# Activate virtual environment
echo "🐍 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📦 Installing/updating dependencies..."
pip install -r requirements.txt

# Run database migrations (including country_code fix)
echo "🗄️ Applying database migrations..."
python migrate_country_code.py

# Update database schema
echo "🔧 Updating database schema..."
python -c "from app import app, db; app.app_context().push(); db.create_all()"

echo "✅ Deployment complete!"
echo "🔄 Please reload your web app in PythonAnywhere dashboard"
echo "🌐 Your app should be available at http://rsvp13.pythonanywhere.com"
```

Make it executable:
```bash
chmod +x deploy_with_fix.sh
```

---

## 🧪 Post-Deployment Testing

### Test 1: Basic Functionality
1. Visit `http://rsvp13.pythonanywhere.com`
2. Verify the app loads without errors
3. Test user registration
4. Test event creation

### Test 2: Database Fix Verification
1. Register a new user with country code
2. Verify the user can be saved without database errors
3. Check that existing users have country codes

### Test 3: Admin Functions
1. Login as admin
2. Test member management
3. Test event management
4. Verify all features work

---

## 🆘 Troubleshooting

### Common Issues:

1. **Database Error**: If you still get `country_code` errors:
   ```bash
   cd /home/rsvp13/app.course.rsvp/eventapp
   python migrate_country_code.py
   ```

2. **Import Errors**: Check Python path in WSGI configuration

3. **Static Files**: Verify static file mappings in Web tab

4. **Environment**: Check `.env` file exists and is readable

### Debug Commands:
```bash
# Check error logs
tail -f /var/log/rsvp13.pythonanywhere.com.error.log

# Test app locally on PythonAnywhere
cd /home/rsvp13/app.course.rsvp/eventapp
source venv/bin/activate
python app.py
```

---

## 🎉 Success!

Once deployed successfully, your EventApp will be available at:
**http://rsvp13.pythonanywhere.com**

### Key Features Working:
- ✅ User registration with country codes
- ✅ Event management
- ✅ RSVP system
- ✅ Admin panel
- ✅ Database integrity

### Future Updates:
To update your app in the future:
```bash
cd /home/rsvp13/app.course.rsvp/eventapp
./deploy_with_fix.sh
```

Then reload your web app in PythonAnywhere dashboard.

---

## 📞 Support

If you encounter any issues:
1. Check PythonAnywhere error logs
2. Verify database migrations completed
3. Ensure all file paths are correct
4. Restart the web application

Your EventApp is now ready for production! 🚀
