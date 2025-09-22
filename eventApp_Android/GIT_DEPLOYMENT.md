# 🚀 Git Deployment Guide for PythonAnywhere

## Overview
This guide shows you how to connect your local EventApp development with PythonAnywhere using Git for efficient deployment and updates.

## 📋 Prerequisites
- PythonAnywhere account (free or paid)
- Git repository (GitHub, GitLab, or Bitbucket)
- Your EventApp code ready for deployment

---

## 🔧 Step 1: Prepare Your Local Repository

### 1.1 Initialize Git Repository (if not already done)
```bash
# Navigate to your project directory
cd D:\GitHub\app.course.rsvp\eventapp

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial EventApp commit with all features"
```

### 1.2 Create .gitignore File
Create a `.gitignore` file to exclude sensitive files:

```gitignore
# Environment variables
.env
.env.local
.env.production

# Database files
*.db
*.sqlite
*.sqlite3
instance/

# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so

# Virtual environment
venv/
env/
ENV/

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Logs
*.log

# Temporary files
*.tmp
*.temp
```

### 1.3 Push to Remote Repository
```bash
# Add remote repository (replace with your repository URL)
git remote add origin https://github.com/yourusername/eventapp.git

# Push to remote
git push -u origin main
```

---

## 🌐 Step 2: Set Up PythonAnywhere

### 2.1 Create New Web App
1. Log into PythonAnywhere
2. Go to **Web** tab
3. Click **Add a new web app**
4. Choose **Flask** framework
5. Select **Python 3.11** (or latest available)
6. Choose a domain name

### 2.2 Clone Your Repository
1. Open a **Bash console** on PythonAnywhere
2. Navigate to your home directory:
   ```bash
   cd /home/yourusername
   ```
3. Clone your repository:
   ```bash
   git clone https://github.com/yourusername/eventapp.git
   ```
4. Navigate to the project:
   ```bash
   cd eventapp
   ```

### 2.3 Set Up Virtual Environment
```bash
# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## ⚙️ Step 3: Configure PythonAnywhere Web App

### 3.1 Update WSGI Configuration
1. Go to **Web** tab in PythonAnywhere
2. Click on your web app
3. Click **WSGI configuration file**
4. Replace the content with:

```python
import sys
import os

# Add your project directory to Python path
path = '/home/yourusername/eventapp'
if path not in sys.path:
    sys.path.append(path)

# Import your Flask app
from app import app as application

# Set environment variables
os.environ['FLASK_ENV'] = 'production'
```

### 3.2 Configure Static Files
In the **Web** tab, set:
- **Static files**: `/home/yourusername/eventapp/static/` → `/static/`
- **Static files**: `/home/yourusername/eventapp/static/images/` → `/static/images/`

### 3.3 Set Working Directory
Set the working directory to: `/home/yourusername/eventapp`

---

## 🔐 Step 4: Environment Configuration

### 4.1 Create Production Environment File
Create `.env` file in your PythonAnywhere project directory:

```bash
# In PythonAnywhere Bash console
cd /home/yourusername/eventapp
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
cd /home/yourusername/eventapp
source venv/bin/activate

# Create database tables
python app.py

# Set up admin user
python setup_admin.py
```

### 5.2 Reload Web App
1. Go to **Web** tab in PythonAnywhere
2. Click **Reload** button
3. Visit your website URL

---

## 🔄 Step 6: Automated Deployment Workflow

### 6.1 Create Deployment Script
Create `deploy.sh` in your project root:

```bash
#!/bin/bash
# Deployment script for PythonAnywhere

echo "🚀 Starting deployment..."

# Pull latest changes
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt

# Run database migrations (if any)
python -c "from app import app, db; app.app_context().push(); db.create_all()"

echo "✅ Deployment complete!"
echo "🔄 Please reload your web app in PythonAnywhere dashboard"
```

### 6.2 Make Script Executable
```bash
chmod +x deploy.sh
```

### 6.3 Local Development Workflow
```bash
# 1. Make changes to your code
# 2. Test locally
python app.py

# 3. Commit changes
git add .
git commit -m "Add new feature: event images"

# 4. Push to repository
git push origin main

# 5. Deploy to PythonAnywhere
# SSH into PythonAnywhere and run:
cd /home/yourusername/eventapp
./deploy.sh
```

---

## 🔧 Step 7: Advanced Git Integration

### 7.1 GitHub Actions (Optional)
Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to PythonAnywhere

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to PythonAnywhere
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: ${{ secrets.PYTHONANYWHERE_HOST }}
        username: ${{ secrets.PYTHONANYWHERE_USERNAME }}
        key: ${{ secrets.PYTHONANYWHERE_SSH_KEY }}
        script: |
          cd /home/${{ secrets.PYTHONANYWHERE_USERNAME }}/eventapp
          git pull origin main
          source venv/bin/activate
          pip install -r requirements.txt
          python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### 7.2 Webhook Deployment (Alternative)
1. Set up a webhook in your Git repository
2. Create a simple endpoint in your Flask app to handle deployment
3. Use PythonAnywhere's API to reload the web app

---

## 📝 Step 8: Best Practices

### 8.1 Branch Strategy
```bash
# Create feature branches
git checkout -b feature/event-images
# Make changes
git add .
git commit -m "Add event images feature"
git push origin feature/event-images

# Merge to main when ready
git checkout main
git merge feature/event-images
git push origin main
```

### 8.2 Environment Management
- Keep `.env` files out of version control
- Use different branches for different environments
- Test changes locally before deploying

### 8.3 Database Management
```bash
# Backup database before major changes
cp eventapp.db eventapp_backup.db

# Create database migrations
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

---

## 🆘 Troubleshooting

### Common Issues:

1. **Import Errors**: Check Python path in WSGI configuration
2. **Static Files Not Loading**: Verify static file mappings
3. **Database Issues**: Ensure database file permissions
4. **Environment Variables**: Check `.env` file exists and is readable

### Debug Commands:
```bash
# Check PythonAnywhere logs
tail -f /var/log/yourusername.pythonanywhere.com.error.log

# Test Flask app locally on PythonAnywhere
cd /home/yourusername/eventapp
source venv/bin/activate
python app.py
```

---

## 🎉 Benefits of Git Deployment

✅ **Version Control**: Track all changes and rollback if needed
✅ **Collaboration**: Multiple developers can work on the project
✅ **Automation**: Set up automated deployment pipelines
✅ **Backup**: Your code is safely stored in Git repository
✅ **Efficiency**: Deploy changes with simple `git push` commands
✅ **Testing**: Test changes locally before deploying

---

## 📞 Support

If you encounter any issues:
1. Check PythonAnywhere's documentation
2. Review your Git repository settings
3. Verify environment variables and file permissions
4. Check PythonAnywhere's error logs

**Happy Deploying! 🚀**
