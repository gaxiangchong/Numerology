# 🚀 PythonAnywhere Deployment Guide for event.mynoblequest.com

## 📋 Pre-Deployment Checklist

### ✅ **Before You Start**
- [ ] Domain `event.mynoblequest.com` is registered and configured
- [ ] DNS points to PythonAnywhere
- [ ] PythonAnywhere account has the domain added
- [ ] You have access to PythonAnywhere console
- [ ] Your code is committed to Git (✅ Done!)

## 🛠️ Step-by-Step Deployment

### **Step 1: Access PythonAnywhere Console**

1. **Login to PythonAnywhere**
   - Go to [pythonanywhere.com](https://pythonanywhere.com)
   - Login with your credentials

2. **Open Bash Console**
   - Click on "Consoles" tab
   - Click "Bash" to open a new console

### **Step 2: Navigate to Your Project**

```bash
# Navigate to your project directory
cd /home/rsvp13/app.course.rsvp/eventapp

# Check current status
pwd
ls -la
```

### **Step 3: Pull Latest Changes from Git**

```bash
# Pull the latest changes from your repository
git pull origin main

# Verify the new files are there
ls -la | grep -E "(wsgi_event_mynoblequest|deploy_event_mynoblequest|env_event_mynoblequest)"
```

### **Step 4: Set Up Environment Variables**

```bash
# Create .env file with your domain configuration
nano .env
```

**Copy and paste this content into the .env file:**

```bash
# Flask Configuration
SECRET_KEY=your-secure-secret-key-here-change-this
SERVER_NAME=event.mynoblequest.com
APPLICATION_ROOT=/

# Database Configuration
DATABASE_URL=sqlite:///eventapp.db

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
ADMIN_EMAIL=noblequest.edu@outlook.com

# Stripe Configuration (if using payments)
STRIPE_PUBLISHABLE_KEY=pk_live_your_publishable_key
STRIPE_SECRET_KEY=sk_live_your_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Domain-specific settings
DOMAIN=event.mynoblequest.com
BASE_URL=https://event.mynoblequest.com
```

**Important:** Replace the placeholder values with your actual credentials!

### **Step 5: Run Database Migrations**

```bash
# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt

# Run the country_code migration
python migrate_country_code.py

# Create/update database tables
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### **Step 6: Configure Web App in PythonAnywhere Dashboard**

1. **Go to Web Tab**
   - Click on "Web" tab in PythonAnywhere dashboard

2. **Add New Web App**
   - Click "Add a new web app"
   - Select "Manual configuration"
   - Choose Python 3.10

3. **Configure the Web App**
   - **Source code**: `/home/rsvp13/app.course.rsvp/eventapp`
   - **Working directory**: `/home/rsvp13/app.course.rsvp/eventapp`
   - **WSGI file**: `/home/rsvp13/app.course.rsvp/eventapp/wsgi_event_mynoblequest.py`

### **Step 7: Set Up WSGI File**

```bash
# Copy the WSGI file to the correct location
cp wsgi_event_mynoblequest.py /var/www/event_mynoblequest_com_wsgi.py

# Set proper permissions
chmod 644 /var/www/event_mynoblequest_com_wsgi.py
```

### **Step 8: Test the Application**

1. **Reload Web App**
   - Go to "Web" tab in PythonAnywhere
   - Click "Reload" button

2. **Check for Errors**
   - Click "Error log" to see any issues
   - Fix any errors that appear

3. **Test the Domain**
   - Visit `https://event.mynoblequest.com`
   - Test login/registration
   - Test event creation
   - Test RSVP functionality

### **Step 9: Run Deployment Script (Recommended)**

```bash
# Make the script executable
chmod +x deploy_event_mynoblequest.sh

# Run the deployment script
./deploy_event_mynoblequest.sh
```

## 🔧 Configuration Details

### **WSGI File Content**

The WSGI file should contain:
```python
#!/usr/bin/env python3
"""
WSGI configuration for event.mynoblequest.com
"""

import sys
import os

# Add the project directory to Python path
project_dir = '/home/rsvp13/app.course.rsvp/eventapp'
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

# Change to the project directory
os.chdir(project_dir)

# Set environment variables for the new domain
os.environ['SERVER_NAME'] = 'event.mynoblequest.com'
os.environ['APPLICATION_ROOT'] = '/'

# Import the Flask application
from app import app as application

if __name__ == "__main__":
    application.run()
```

### **Environment Variables Explained**

```bash
# Flask Configuration
SECRET_KEY=your-secure-secret-key-here-change-this  # Generate a strong secret key
SERVER_NAME=event.mynoblequest.com                # Your domain
APPLICATION_ROOT=/                                  # Root path

# Database Configuration
DATABASE_URL=sqlite:///eventapp.db                  # SQLite database path

# Email Configuration
MAIL_SERVER=smtp.gmail.com                          # Gmail SMTP server
MAIL_PORT=587                                       # Gmail SMTP port
MAIL_USE_TLS=True                                   # Use TLS encryption
MAIL_USERNAME=your-email@gmail.com                  # Your Gmail address
MAIL_PASSWORD=your-app-password                     # Gmail app password
ADMIN_EMAIL=noblequest.edu@outlook.com              # Admin email for notifications

# Domain-specific settings
DOMAIN=event.mynoblequest.com                       # Your domain
BASE_URL=https://event.mynoblequest.com             # Full URL
```

## 🚨 Troubleshooting

### **Common Issues and Solutions**

#### **1. Domain Not Accessible**
```bash
# Check if domain is properly configured
ping event.mynoblequest.com

# Check DNS resolution
nslookup event.mynoblequest.com
```

**Solution:**
- Verify domain is added to PythonAnywhere account
- Check DNS configuration
- Wait for DNS propagation (up to 24 hours)

#### **2. Application Not Loading**
```bash
# Check PythonAnywhere error logs
# Go to Web tab > Error log

# Check if all dependencies are installed
pip list

# Check if database exists
ls -la *.db
```

**Solution:**
- Verify WSGI file path is correct
- Check all environment variables are set
- Ensure all dependencies are installed

#### **3. Database Issues**
```bash
# Run database migrations
python migrate_country_code.py

# Create database tables
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# Check database file permissions
ls -la *.db
chmod 644 *.db
```

**Solution:**
- Run all migrations
- Check database file permissions
- Verify database path in configuration

#### **4. Email Not Working**
```bash
# Test email configuration
python -c "
from app import app
with app.app_context():
    from app import send_email
    send_email('test@example.com', 'Test Subject', 'Test message')
"
```

**Solution:**
- Verify Gmail credentials
- Check if app password is used (not regular password)
- Test SMTP connection

#### **5. SSL Certificate Issues**
- PythonAnywhere automatically handles SSL
- Wait a few minutes after domain setup
- Check PythonAnywhere dashboard for SSL status

### **Debug Commands**

```bash
# Check application status
ps aux | grep python

# Check error logs
tail -f /var/log/rsvp13.pythonanywhere.com.error.log

# Test database connection
python -c "from app import app, db; app.app_context().push(); print('Database connected:', db.engine.url)"

# Test email configuration
python -c "from app import app; print('Email config:', app.config.get('MAIL_SERVER'))"
```

## 📱 Post-Deployment Testing

### **Test Checklist**

- [ ] **Domain Access**: `https://event.mynoblequest.com` loads correctly
- [ ] **User Registration**: New users can register
- [ ] **User Login**: Existing users can login
- [ ] **Event Creation**: Admins can create events
- [ ] **RSVP Functionality**: Users can RSVP to events
- [ ] **Email Verification**: Email verification works
- [ ] **Password Reset**: Password reset functionality works
- [ ] **Admin Features**: Admin dashboard is accessible
- [ ] **Mobile Responsive**: App works on mobile devices

### **Performance Optimization**

```bash
# Check application performance
# Monitor memory usage
free -h

# Check disk space
df -h

# Monitor application logs
tail -f /var/log/rsvp13.pythonanywhere.com.error.log
```

## 🔄 Future Updates

### **Deploying Updates**

```bash
# Pull latest changes
git pull origin main

# Install new dependencies (if any)
pip install -r requirements.txt

# Run any new migrations
python migrate_country_code.py

# Reload web app in PythonAnywhere dashboard
```

### **Backup Strategy**

```bash
# Backup database
cp eventapp.db eventapp_backup_$(date +%Y%m%d_%H%M%S).db

# Backup environment variables
cp .env .env_backup_$(date +%Y%m%d_%H%M%S)
```

## 📞 Support

If you encounter issues:

1. **Check PythonAnywhere Error Logs**
   - Go to Web tab > Error log
   - Look for specific error messages

2. **Verify Configuration**
   - Check all environment variables
   - Verify file paths
   - Test database connection

3. **Test Components Individually**
   - Test database access
   - Test email functionality
   - Test web app loading

## 🎉 Success!

Once deployed successfully, your EventApp will be available at:
**https://event.mynoblequest.com**

Your users can now access your event management platform with your custom domain! 🚀

### **Next Steps:**
1. Test all functionality
2. Monitor performance
3. Set up regular backups
4. Plan for future updates

Happy deploying! 🎯
