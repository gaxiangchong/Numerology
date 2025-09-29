# Quick Deployment Guide for bazipro.pythonanywhere.com

## 🚀 Step-by-Step Instructions

### **Step 1: Create GitHub Repository**

1. **Go to:** https://github.com/new
2. **Repository name:** `numerology-pwa`
3. **Description:** `Numerology Analysis Tool - PWA with Android support`
4. **Make it Public** (or Private if you prefer)
5. **Click:** "Create repository"

### **Step 2: Push Your Code to GitHub**

```bash
# Add all files (excluding node_modules)
git add .

# Create initial commit
git commit -m "Initial commit: Numerology PWA ready for deployment"

# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/numerology-pwa.git

# Push to GitHub
git push -u origin main
```

### **Step 3: Sign Up for PythonAnywhere**

1. **Go to:** https://www.pythonanywhere.com/
2. **Click:** "Start a new PythonAnywhere account"
3. **Username:** `bazipro` (if available)
4. **Choose:** Free account (or paid for production)
5. **Complete registration**

### **Step 4: Deploy on PythonAnywhere**

#### A. Clone Your Repository
1. **Open PythonAnywhere Console**
2. **Run:**
```bash
git clone https://github.com/gaxiangchong/Numerology.git
cd Numerology
```

#### B. Set Up Environment
```bash
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
   - **Directory:** `/home/bazipro/Numerology/NumberEnergy/mysite/static`

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

#### C. Test Stripe Integration
- ✅ **Payment buttons work**
- ✅ **Checkout process works**
- ✅ **Webhook receives events**

### **Step 6: Update Stripe Webhook**

1. **Go to:** Stripe Dashboard → Webhooks
2. **Update endpoint:** `https://bazipro.pythonanywhere.com/stripe/webhook`
3. **Test webhook** to ensure it works

### **Step 7: Update Android Studio**

```bash
# Update Capacitor configuration
npx cap sync

# Open in Android Studio
npx cap open android
```

## 🎯 Success Checklist

- ✅ **GitHub repository** created and pushed
- ✅ **PythonAnywhere** account set up
- ✅ **Web app** deployed and running
- ✅ **Database** configured
- ✅ **Static files** serving correctly
- ✅ **PWA features** working
- ✅ **Stripe integration** functional
- ✅ **Android app** ready for testing

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

## 📱 Final Result

Your Numerology PWA will be live at:
**https://bazipro.pythonanywhere.com**

With full PWA features:
- ✅ **Installable** on mobile devices
- ✅ **Offline support** with service worker
- ✅ **App-like experience** in standalone mode
- ✅ **Stripe payments** working
- ✅ **Android app** ready for Google Play Store

## 🚀 Next Steps

1. **Test everything** thoroughly
2. **Update Android Studio** with production URL
3. **Submit to Google Play Store**
4. **Monitor and maintain** your live app

Your Numerology PWA is now ready for the world! 🌐📱
