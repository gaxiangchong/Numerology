# Step-by-Step Deployment Guide for bazipro.pythonanywhere.com

## 🚀 Complete Deployment Process

### **Step 1: Initialize Git Repository**

```bash
# Initialize Git repository
git init

# Add all files to Git
git add .

# Create initial commit
git commit -m "Initial commit: Numerology PWA ready for deployment"
```

### **Step 2: Create GitHub Repository**

1. **Go to:** https://github.com/new
2. **Repository name:** `numerology-pwa`
3. **Description:** `Numerology Analysis Tool - PWA with Android support`
4. **Visibility:** Public (or Private if you prefer)
5. **Click:** "Create repository"

### **Step 3: Connect Local Repository to GitHub**

```bash
# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/numerology-pwa.git

# Push to GitHub
git push -u origin main
```

### **Step 4: Deploy to PythonAnywhere**

#### A. Sign Up for PythonAnywhere
1. **Go to:** https://www.pythonanywhere.com/
2. **Sign up** with your email
3. **Choose:** Free account (or paid for production)
4. **Username:** `bazipro` (if available)

#### B. Clone Repository on PythonAnywhere
1. **Open PythonAnywhere Console**
2. **Run these commands:**
```bash
# Clone your repository
git clone https://github.com/YOUR_USERNAME/numerology-pwa.git
cd numerology-pwa

# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### C. Set Up Database
```bash
# Create database
cd mysite
python create_db.py
python manage.py db upgrade
```

#### D. Configure Web App
1. **Go to:** Web tab in PythonAnywhere dashboard
2. **Click:** "Add a new web app"
3. **Choose:** "Manual configuration"
4. **Python version:** 3.10

#### E. Configure WSGI File
1. **Click:** "WSGI configuration file"
2. **Replace content** with:
```python
#!/usr/bin/python3.10
import sys
import os

# Add your project directory to the Python path
path = '/home/bazipro/numerology-pwa'
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

#### F. Configure Static Files
1. **Go to:** Static files section
2. **Add mapping:**
   - **URL:** `/static/`
   - **Directory:** `/home/bazipro/numerology-pwa/mysite/static/`

#### G. Set Environment Variables
1. **Go to:** Environment variables section
2. **Add:**
```
SECRET_KEY=your-secret-key-here
STRIPE_SECRET_KEY=sk_test_your-stripe-secret-key
STRIPE_PUBLISHABLE_KEY=pk_test_your-stripe-publishable-key
STRIPE_WEBHOOK_SECRET=whsec_your-webhook-secret
```

#### H. Reload Web App
1. **Click:** "Reload" button
2. **Wait for** reload to complete
3. **Visit:** https://bazipro.pythonanywhere.com

### **Step 5: Test Your Deployment**

#### A. Test Basic Functionality
- ✅ **Homepage loads**
- ✅ **User registration works**
- ✅ **Login works**
- ✅ **Number analysis works**

#### B. Test PWA Features
- ✅ **Install prompt appears**
- ✅ **App can be installed**
- ✅ **Offline functionality works**
- ✅ **App-like experience**

#### C. Test Stripe Integration
- ✅ **Payment buttons work**
- ✅ **Checkout process works**
- ✅ **Webhook receives events**

### **Step 6: Update Android Studio**

#### A. Sync Capacitor with Production URL
```bash
# Update Capacitor configuration
npx cap sync

# Open in Android Studio
npx cap open android
```

#### B. Test Android App
1. **Build and run** in Android Studio
2. **Test with production server**
3. **Verify all features work**

### **Step 7: Monitor and Maintain**

#### A. Check Logs
1. **Go to:** PythonAnywhere dashboard
2. **Check:** Error logs and access logs
3. **Monitor:** Performance and usage

#### B. Regular Updates
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Update database schema
python mysite/manage.py db upgrade
```

## 🔧 Troubleshooting

### Common Issues:

#### 1. Import Errors
- **Check:** Python path in WSGI file
- **Verify:** All dependencies installed
- **Solution:** `pip install -r requirements.txt`

#### 2. Database Issues
- **Check:** Database file permissions
- **Solution:** `chmod 644 instance/users.db`

#### 3. Static Files Not Loading
- **Check:** Static file mapping
- **Verify:** File permissions
- **Solution:** Clear browser cache

#### 4. Stripe Webhook Issues
- **Update:** Webhook URL in Stripe dashboard
- **New URL:** `https://bazipro.pythonanywhere.com/stripe/webhook`
- **Test:** Webhook with Stripe CLI

## 📱 Final Steps

### 1. Update Stripe Webhook
1. **Go to:** Stripe Dashboard → Webhooks
2. **Update endpoint:** `https://bazipro.pythonanywhere.com/stripe/webhook`
3. **Test webhook** to ensure it works

### 2. Test PWA Installation
1. **Visit:** https://bazipro.pythonanywhere.com
2. **Look for:** Install button in browser
3. **Test:** App installation and offline functionality

### 3. Submit to App Stores
1. **Update Android Studio** with production URL
2. **Test Android app** thoroughly
3. **Submit to Google Play Store**

## 🎯 Success Checklist

- ✅ **Git repository** created and pushed
- ✅ **PythonAnywhere** account set up
- ✅ **Web app** deployed and running
- ✅ **Database** configured
- ✅ **Static files** serving correctly
- ✅ **PWA features** working
- ✅ **Stripe integration** functional
- ✅ **Android app** ready for testing

Your Numerology PWA is now live at **https://bazipro.pythonanywhere.com**! 🚀🌐
