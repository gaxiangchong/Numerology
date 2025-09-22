# PythonAnywhere Deployment Guide for Numerology PWA

## 🚀 Overview
This guide will help you deploy your Numerology PWA Flask application to PythonAnywhere, making it accessible worldwide with HTTPS support.

## 📋 Prerequisites

### 1. PythonAnywhere Account
- **Free Account:** Limited but sufficient for testing
- **Paid Account:** Recommended for production (starts at $5/month)
- **Sign up:** https://www.pythonanywhere.com/

### 2. Prepare Your Local App
- ✅ Flask app working locally
- ✅ Database migrations completed
- ✅ Static files organized
- ✅ Environment variables identified

## 🛠️ Step-by-Step Deployment

### Step 1: Create PythonAnywhere Account
1. **Go to:** https://www.pythonanywhere.com/
2. **Click:** "Start a new PythonAnywhere account"
3. **Choose:** Free account (or paid for production)
4. **Complete registration**

### Step 2: Prepare Your Flask App for Production

#### A. Create Production Requirements File
```bash
# In your project root
pip freeze > requirements.txt
```

#### B. Create WSGI Configuration File
Create `wsgi.py` in your project root:
```python
#!/usr/bin/python3.10
import sys
import os

# Add your project directory to the Python path
path = '/home/yourusername/numerology-app'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['FLASK_ENV'] = 'production'
os.environ['FLASK_APP'] = 'mysite/app.py'

# Import your Flask app
from mysite.app import app as application

if __name__ == "__main__":
    application.run()
```

#### C. Create Production Configuration
Create `config.py`:
```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///instance/users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Stripe Configuration
    STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
    STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')
    
    # Flask Configuration
    FLASK_ENV = 'production'
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    DEBUG = False
    FLASK_ENV = 'production'
```

### Step 3: Upload Your Code to PythonAnywhere

#### Method 1: Using Git (Recommended)
```bash
# In your local project
git init
git add .
git commit -m "Initial commit for production"

# Push to GitHub/GitLab
git remote add origin https://github.com/yourusername/numerology-app.git
git push -u origin main
```

Then on PythonAnywhere:
```bash
# In PythonAnywhere console
git clone https://github.com/yourusername/numerology-app.git
cd numerology-app
```

#### Method 2: Using PythonAnywhere File Manager
1. **Go to:** Files tab in PythonAnywhere dashboard
2. **Create folder:** `numerology-app`
3. **Upload files** using the file manager
4. **Extract zip files** if needed

### Step 4: Set Up Virtual Environment
```bash
# In PythonAnywhere console
cd numerology-app
python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5: Configure Database
```bash
# In PythonAnywhere console
cd numerology-app
source venv/bin/activate
python mysite/create_db.py
python mysite/manage.py db upgrade
```

### Step 6: Set Environment Variables
In PythonAnywhere dashboard:
1. **Go to:** Web tab
2. **Click:** "Environment variables"
3. **Add:**
   ```
   SECRET_KEY=your-secret-key-here
   STRIPE_SECRET_KEY=sk_test_your-stripe-secret-key
   STRIPE_PUBLISHABLE_KEY=pk_test_your-stripe-publishable-key
   STRIPE_WEBHOOK_SECRET=whsec_your-webhook-secret
   ```

### Step 7: Configure WSGI File
1. **Go to:** Web tab in PythonAnywhere dashboard
2. **Click:** "WSGI configuration file"
3. **Replace content** with:
```python
#!/usr/bin/python3.10
import sys
import os

# Add your project directory to the Python path
path = '/home/yourusername/numerology-app'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['FLASK_ENV'] = 'production'
os.environ['FLASK_APP'] = 'mysite/app.py'

# Import your Flask app
from mysite.app import app as application

if __name__ == "__main__":
    application.run()
```

### Step 8: Configure Static Files
1. **Go to:** Web tab
2. **Click:** "Static files"
3. **Add mapping:**
   - **URL:** `/static/`
   - **Directory:** `/home/yourusername/numerology-app/mysite/static/`

### Step 9: Set Up Domain and SSL
1. **Go to:** Web tab
2. **Set domain:** `yourusername.pythonanywhere.com`
3. **Enable HTTPS:** Check "Force HTTPS"
4. **Click:** "Reload" to apply changes

### Step 10: Test Your Deployment
1. **Visit:** `https://yourusername.pythonanywhere.com`
2. **Test all features:**
   - User registration/login
   - Number analysis
   - Stripe payments
   - PWA installation

## 🔧 Production Optimizations

### 1. Update Stripe Webhook URL
In your Stripe Dashboard:
1. **Go to:** Webhooks
2. **Update endpoint URL:** `https://yourusername.pythonanywhere.com/stripe/webhook`
3. **Test webhook** to ensure it works

### 2. Configure PWA for Production
Update `mysite/static/manifest.json`:
```json
{
  "name": "Numerology Analysis Tool",
  "short_name": "Numerology",
  "start_url": "https://yourusername.pythonanywhere.com/",
  "scope": "https://yourusername.pythonanywhere.com/",
  "display": "standalone",
  "background_color": "#1a1a1a",
  "theme_color": "#3b82f6"
}
```

### 3. Update Capacitor Config
Update `capacitor.config.json`:
```json
{
  "appId": "com.numerology.analysis",
  "appName": "Numerology Analysis",
  "webDir": "mysite/static",
  "server": {
    "url": "https://yourusername.pythonanywhere.com",
    "cleartext": false
  }
}
```

## 📱 PWA Deployment for Android Studio

### 1. Update Your Local Config
```bash
# Update capacitor config with production URL
npx cap sync
```

### 2. Test PWA Features
- **Install prompt** should work
- **Offline functionality** should work
- **App-like experience** should be smooth

## 🚨 Troubleshooting

### Common Issues:

#### 1. Import Errors
```bash
# Check Python path in WSGI file
# Ensure all dependencies are installed
pip install -r requirements.txt
```

#### 2. Database Issues
```bash
# Recreate database
rm instance/users.db
python mysite/create_db.py
python mysite/manage.py db upgrade
```

#### 3. Static Files Not Loading
- **Check static file mapping** in PythonAnywhere
- **Verify file permissions**
- **Clear browser cache**

#### 4. Stripe Webhook Issues
- **Check webhook URL** in Stripe dashboard
- **Verify HTTPS** is working
- **Test webhook** with Stripe CLI

### Debugging Steps:
1. **Check PythonAnywhere logs**
2. **Test locally** with production settings
3. **Verify environment variables**
4. **Check database connections**

## 📊 Monitoring and Maintenance

### 1. Monitor Performance
- **Check PythonAnywhere dashboard** regularly
- **Monitor CPU usage** and memory
- **Check error logs**

### 2. Regular Updates
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Update database schema
python mysite/manage.py db upgrade
```

### 3. Backup Strategy
- **Export database** regularly
- **Backup code** to Git
- **Document configuration** changes

## 🎯 Next Steps After Deployment

### 1. Test Everything
- ✅ User registration/login
- ✅ Number analysis functionality
- ✅ Stripe payment processing
- ✅ PWA installation
- ✅ Mobile responsiveness

### 2. Update Android Studio
- **Update Capacitor config** with production URL
- **Test Android app** with live server
- **Submit to Google Play Store**

### 3. Monitor and Optimize
- **Monitor user feedback**
- **Optimize performance**
- **Add new features**

## 💰 Cost Breakdown

### PythonAnywhere Pricing:
- **Free:** $0/month (limited)
- **Hacker:** $5/month (recommended)
- **Web Developer:** $10/month (more resources)

### Additional Costs:
- **Custom Domain:** $10-15/year (optional)
- **SSL Certificate:** Free with PythonAnywhere
- **Stripe Fees:** 2.9% + 30¢ per transaction

Your Numerology PWA will now be live on the internet with HTTPS support! 🚀🌐
