# 🚀 Deploy Latest Updates to PythonAnywhere

## 📋 What's New in This Update

Your EventApp now includes these latest improvements:

✅ **Email Verification System**
- Users must verify email before logging in
- SendGrid email integration working
- Verification links with 24-hour expiration

✅ **UI/UX Improvements**
- Purple gradient backgrounds for welcome sections
- Red-to-purple gradient logo
- Modern, professional appearance

✅ **Enhanced Resend Verification**
- 1-minute cooldown timer
- Proper success messages
- Admin contact information
- Better user guidance

---

## 🔄 Step 1: Commit and Push Your Local Changes

First, make sure all your local changes are committed and pushed to GitHub:

```bash
# In your local project directory
git add .
git commit -m "Add email verification, UI improvements, and resend timer"
git push origin main
```

---

## 🖥️ Step 2: Access PythonAnywhere

1. **Go to PythonAnywhere**: https://www.pythonanywhere.com
2. **Log in** with your account (`rsvp13`)
3. **Open a Bash console**

---

## 📥 Step 3: Run the Update Script

Copy and paste this command in your PythonAnywhere Bash console:

```bash
cd /home/rsvp13/app.course.rsvp/eventapp && curl -sSL https://raw.githubusercontent.com/gaxiangchong/app.course.rsvp/main/eventapp/deploy_latest_updates.sh | bash
```

**OR** if you prefer to run it manually:

```bash
# Navigate to your project
cd /home/rsvp13/app.course.rsvp/eventapp

# Pull latest changes
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Update dependencies
pip install -r requirements.txt

# Update .env for production
cat > .env << 'EOF'
# EventApp Environment Configuration
# Generated for SendGrid email service

# Flask Configuration
SECRET_KEY=$(python3.11 -c "import secrets; print(secrets.token_hex(32))")
FLASK_ENV=production
DATABASE_URL=sqlite:///eventapp.db

# Flask URL Configuration (for email verification)
SERVER_NAME=rsvp13.pythonanywhere.com
APPLICATION_ROOT=/
PREFERRED_URL_SCHEME=https

# Email Configuration (SendGrid)
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=apikey
MAIL_PASSWORD=YOUR_SENDGRID_API_KEY_HERE

# App Configuration
APP_NAME=EventApp
ADMIN_EMAIL=noblequest.edu@outlook.com
EOF

# Update database
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# Set permissions
chmod -R 755 /home/rsvp13/app.course.rsvp/eventapp
```

---

## ⚙️ Step 4: Update Web App Configuration

1. **Go to Web tab** in PythonAnywhere dashboard
2. **Click on your web app**
3. **Update WSGI configuration file** with this content:

```python
# This file contains the WSGI configuration required to serve up your
# EventApp web application at http://rsvp13.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.

import sys
import os

# Add your project directory to the sys.path
project_home = '/home/rsvp13/app.course.rsvp/eventapp'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment variables for production
os.environ['FLASK_ENV'] = 'production'

# Import your Flask app but need to call it "application" for WSGI to work
from app import app as application  # noqa
```

4. **Set Working Directory**: `/home/rsvp13/app.course.rsvp/eventapp`
5. **Static File Mappings**:
   - `/static/` → `/home/rsvp13/app.course.rsvp/eventapp/static/`

---

## 🔄 Step 5: Reload Your Web App

1. **Go to Web tab**
2. **Click the "Reload" button**
3. **Wait for the reload to complete**

---

## 🧪 Step 6: Test Your Updated App

Visit your app: **https://rsvp13.pythonanywhere.com**

### Test These Features:

1. **Registration & Email Verification**:
   - Register a new account
   - Check email for verification link
   - Click verification link
   - Try logging in

2. **UI Improvements**:
   - Check purple gradient backgrounds
   - Verify red-to-purple logo gradient
   - Test responsive design

3. **Resend Verification**:
   - Try resending verification email
   - Check 1-minute timer works
   - Verify admin contact info is shown

---

## 🆘 Troubleshooting

### If Something Goes Wrong:

1. **Check Error Logs**:
   ```bash
   tail -f /var/log/rsvp13.pythonanywhere.com.error.log
   ```

2. **Test Locally on PythonAnywhere**:
   ```bash
   cd /home/rsvp13/app.course.rsvp/eventapp
   source venv/bin/activate
   python app.py
   ```

3. **Check File Permissions**:
   ```bash
   chmod -R 755 /home/rsvp13/app.course.rsvp/eventapp
   ```

4. **Verify Environment Variables**:
   ```bash
   cat .env
   ```

---

## 📞 Support

If you encounter any issues:

1. **Check PythonAnywhere logs** for error messages
2. **Verify all file paths** are correct
3. **Ensure .env file** has proper email configuration
4. **Test email sending** with a simple registration

---

## 🎉 Success!

Your EventApp is now updated with all the latest features:

- ✅ **Email verification system** working
- ✅ **Beautiful purple gradients** for backgrounds
- ✅ **Red-to-purple logo gradient**
- ✅ **Resend verification with timer**
- ✅ **Professional UI/UX improvements**

**Your app**: https://rsvp13.pythonanywhere.com

---

## 🔄 Future Updates

For future updates, simply:

1. **Push changes to GitHub**
2. **Run the update script** on PythonAnywhere
3. **Reload your web app**

```bash
cd /home/rsvp13/app.course.rsvp/eventapp
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

Then reload your web app in PythonAnywhere dashboard!
