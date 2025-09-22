# 🌐 Domain Update Guide: event.noblequest.com

## 🚀 Overview

This guide helps you update your EventApp from the old PythonAnywhere domain to your new custom domain `event.noblequest.com`.

## 📋 Pre-Deployment Checklist

### ✅ **Domain Setup**
- [ ] Domain `event.noblequest.com` is registered
- [ ] DNS is configured to point to PythonAnywhere
- [ ] SSL certificate is set up (PythonAnywhere handles this automatically)
- [ ] Domain is added to PythonAnywhere account

### ✅ **PythonAnywhere Configuration**
- [ ] Web app is configured for the new domain
- [ ] WSGI file is updated
- [ ] Environment variables are set
- [ ] Database is accessible

## 🛠️ Step-by-Step Deployment

### **Step 1: Update PythonAnywhere Web App**

1. **Go to PythonAnywhere Dashboard**
   - Navigate to "Web" tab
   - Click "Add a new web app"
   - Select "Manual configuration"
   - Choose Python 3.10

2. **Configure the Web App**
   - **Source code**: `/home/rsvp13/app.course.rsvp/eventapp`
   - **Working directory**: `/home/rsvp13/app.course.rsvp/eventapp`
   - **WSGI file**: `/home/rsvp13/app.course.rsvp/eventapp/wsgi_event_noblequest.py`

### **Step 2: Update WSGI Configuration**

1. **Create/Update WSGI File**
   ```bash
   # On PythonAnywhere console
   cd /home/rsvp13/app.course.rsvp/eventapp
   nano wsgi_event_noblequest.py
   ```

2. **Copy the WSGI content** from `wsgi_event_noblequest.py` (created above)

### **Step 3: Set Environment Variables**

1. **Create .env file**
   ```bash
   # On PythonAnywhere console
   cd /home/rsvp13/app.course.rsvp/eventapp
   nano .env
   ```

2. **Copy environment variables** from `env_event_noblequest.txt` (created above)

3. **Update with your actual values**:
   - Replace `your-secure-secret-key-here` with a strong secret key
   - Update email credentials
   - Update Stripe keys if using payments

### **Step 4: Deploy the Application**

1. **Run the deployment script**
   ```bash
   # On PythonAnywhere console
   cd /home/rsvp13/app.course.rsvp/eventapp
   chmod +x deploy_event_noblequest.sh
   ./deploy_event_noblequest.sh
   ```

2. **Or run manually**:
   ```bash
   # Pull latest changes
   git pull origin main
   
   # Activate virtual environment
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run migrations
   python migrate_country_code.py
   
   # Create database tables
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

### **Step 5: Test the Application**

1. **Check the web app**
   - Visit `https://event.noblequest.com`
   - Test login/registration
   - Test event creation
   - Test RSVP functionality

2. **Check email functionality**
   - Test email verification
   - Test password reset
   - Check email notifications

## 🔧 Configuration Details

### **Environment Variables**

```bash
# Flask Configuration
SECRET_KEY=your-secure-secret-key-here
SERVER_NAME=event.noblequest.com
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

# Domain-specific settings
DOMAIN=event.noblequest.com
BASE_URL=https://event.noblequest.com
```

### **WSGI Configuration**

The WSGI file should contain:
```python
#!/usr/bin/env python3
import sys
import os

project_dir = '/home/rsvp13/app.course.rsvp/eventapp'
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

os.chdir(project_dir)
os.environ['SERVER_NAME'] = 'event.noblequest.com'
os.environ['APPLICATION_ROOT'] = '/'

from app import app as application
```

## 🚨 Troubleshooting

### **Common Issues**

1. **Domain not accessible**
   - Check DNS configuration
   - Verify domain is added to PythonAnywhere
   - Wait for DNS propagation (up to 24 hours)

2. **SSL certificate issues**
   - PythonAnywhere automatically handles SSL
   - Wait a few minutes after domain setup
   - Check PythonAnywhere dashboard for SSL status

3. **Application not loading**
   - Check WSGI file path
   - Verify environment variables
   - Check PythonAnywhere error logs

4. **Database issues**
   - Run migrations: `python migrate_country_code.py`
   - Check database file permissions
   - Verify database path in configuration

5. **Email not working**
   - Check email credentials
   - Verify SMTP settings
   - Test with a simple email first

### **Debug Steps**

1. **Check PythonAnywhere logs**
   - Go to "Web" tab
   - Click "Error log" to see any errors

2. **Test locally first**
   - Run the app locally to ensure it works
   - Check all dependencies are installed

3. **Verify file permissions**
   ```bash
   chmod 755 /home/rsvp13/app.course.rsvp/eventapp
   chmod 644 /home/rsvp13/app.course.rsvp/eventapp/*.py
   ```

## 📱 Mobile Optimization

Since you're using the new domain, consider these mobile optimizations:

1. **Add PWA manifest** (optional)
2. **Optimize for mobile devices**
3. **Test on different screen sizes**
4. **Ensure touch-friendly interface**

## 🔄 Post-Deployment

### **After successful deployment:**

1. **Update any external references**
   - Update documentation
   - Update any hardcoded URLs
   - Update email templates if needed

2. **Test all functionality**
   - User registration/login
   - Event creation/management
   - RSVP functionality
   - Email notifications
   - Admin features

3. **Monitor the application**
   - Check error logs regularly
   - Monitor performance
   - Test email delivery

## 📞 Support

If you encounter issues:

1. **Check PythonAnywhere documentation**
2. **Review error logs**
3. **Test components individually**
4. **Verify all configuration settings**

## 🎉 Success!

Once deployed, your EventApp will be available at:
**https://event.noblequest.com**

Your users can now access your event management platform with your custom domain! 🚀
