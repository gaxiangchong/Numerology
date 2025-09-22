# 🚀 Quick Deployment Guide for EventApp

## PythonAnywhere Deployment (5 minutes)

### Step 1: Access PythonAnywhere
1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Log in with your `rsvp13` account
3. Go to the **Web** tab

### Step 2: Run Deployment Script
1. Open a **Bash console** on PythonAnywhere
2. Copy and paste this command:
```bash
curl -sSL https://raw.githubusercontent.com/gaxiangchong/app.course.rsvp/main/eventapp/deploy_to_pythonanywhere.sh | bash
```

**OR** manually run these commands:
```bash
cd /home/rsvp13
git clone https://github.com/gaxiangchong/app.course.rsvp.git
cd app.course.rsvp/eventapp
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -c "from app import app, db; app.app_context().push(); db.create_all()"
python setup_admin.py
```

### Step 3: Configure Web App
1. In PythonAnywhere **Web** tab, click **Add a new web app**
2. Choose **Flask** and **Python 3.11**
3. Set **Source code** to: `/home/rsvp13/app.course.rsvp/eventapp`
4. Set **Working directory** to: `/home/rsvp13/app.course.rsvp/eventapp`

### Step 4: Update WSGI Configuration
1. Click **WSGI configuration file**
2. Replace the content with:
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

Add this content (replace with your actual values):
```env
SECRET_KEY=your-secret-key-here
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
3. Login with admin credentials you created

## 🎉 You're Live!

Your EventApp is now deployed and accessible at:
**http://rsvp13.pythonanywhere.com**

## 🔄 Future Updates
To update your app:
```bash
cd /home/rsvp13/app.course.rsvp/eventapp
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```
Then reload your web app in PythonAnywhere dashboard.

## 🆘 Troubleshooting
- Check error logs in PythonAnywhere Web tab
- Ensure all file paths are correct
- Verify environment variables are set
- Make sure static file mappings are configured
