# NumberEnergy Flask App - Deployment Guide

This guide will help you run your Flask app locally and deploy it to PythonAnywhere.

## 🏠 Running Locally

### Prerequisites
- Python 3.8+ installed
- Git (optional, for version control)

### Step 1: Set up Virtual Environment
```bash
# Navigate to your project directory
cd D:\Github\NumberEnergy

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt
```

### Step 3: Set up Database
```bash
# Navigate to mysite directory
cd mysite

# Initialize database migrations
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

### Step 4: Run the App
You have several options:

**Option A: Using the run script**
```bash
# From project root
python run_local.py
```

**Option B: Using the batch file (Windows)**
```bash
# Double-click run_local.bat or run from command line
run_local.bat
```

**Option C: Direct Flask command**
```bash
# From mysite directory
cd mysite
python app.py
```

### Step 5: Access Your App
Open your browser and go to: `http://127.0.0.1:5000`

## 🌐 Deploying to PythonAnywhere

### Step 1: Prepare Your Code
1. **Update Stripe Keys**: Replace test keys with live keys in `app.py`
2. **Update Domain**: Change `YOUR_DOMAIN` to your PythonAnywhere domain
3. **Set Secret Key**: Use a strong secret key for production

### Step 2: Upload to PythonAnywhere
1. **Via Git (Recommended)**:
   ```bash
   # Push your code to GitHub/GitLab
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   
   # On PythonAnywhere, clone your repository
   git clone https://github.com/yourusername/NumberEnergy.git
   ```

2. **Via File Upload**:
   - Zip your project folder
   - Upload via PythonAnywhere's file manager
   - Extract in your home directory

### Step 3: Set up PythonAnywhere Environment
1. **Open a Bash Console** on PythonAnywhere
2. **Navigate to your project**:
   ```bash
   cd ~/NumberEnergy
   ```

3. **Create Virtual Environment**:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 NumberEnergy
   workon NumberEnergy
   ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Step 4: Configure Database
```bash
# Navigate to mysite directory
cd mysite

# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Step 5: Configure Web App
1. **Go to Web tab** in PythonAnywhere dashboard
2. **Create new web app**:
   - Choose "Manual Configuration"
   - Select Python 3.10
3. **Set Source Code**: `/home/yourusername/NumberEnergy/mysite`
4. **Set Working Directory**: `/home/yourusername/NumberEnergy/mysite`
5. **Set Virtualenv**: `/home/yourusername/.virtualenvs/NumberEnergy`

### Step 6: Configure WSGI File
Edit the WSGI file (usually `/var/www/yourusername_pythonanywhere_com_wsgi.py`):

```python
import sys
import os

# Add your project directory to the Python path
path = '/home/yourusername/NumberEnergy/mysite'
if path not in sys.path:
    sys.path.append(path)

# Import your Flask app
from app import app as application

if __name__ == "__main__":
    application.run()
```

### Step 7: Set up Static Files
In the Web tab, add a static files mapping:
- **URL**: `/static/`
- **Directory**: `/home/yourusername/NumberEnergy/mysite/static/`

### Step 8: Configure Environment Variables
In the Web tab, add these environment variables:
```
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your_production_secret_key
STRIPE_SECRET_KEY=sk_live_your_live_stripe_key
YOUR_DOMAIN=https://yourusername.pythonanywhere.com
```

### Step 9: Set up Stripe Webhooks
1. **In Stripe Dashboard**:
   - Go to Webhooks
   - Add endpoint: `https://yourusername.pythonanywhere.com/stripe/webhook`
   - Select events: `invoice.paid`
   - Copy the webhook secret

2. **Update your app** with the webhook secret

### Step 10: Reload and Test
1. **Reload your web app** in PythonAnywhere
2. **Test your app** at `https://yourusername.pythonanywhere.com`

## 🔧 Troubleshooting

### Common Issues:

1. **Import Errors**:
   - Check that all dependencies are installed
   - Verify Python path in WSGI file

2. **Database Issues**:
   - Ensure database migrations are applied
   - Check file permissions on database file

3. **Static Files Not Loading**:
   - Verify static files mapping in Web tab
   - Check file paths are correct

4. **Stripe Webhook Issues**:
   - Verify webhook URL is accessible
   - Check webhook secret is correct

### Logs:
- **Application logs**: Available in PythonAnywhere's Web tab
- **Error logs**: Check the Error log section
- **Server logs**: Available in the Log files section

## 📝 Important Notes

1. **Security**: Never commit API keys or secrets to version control
2. **Database**: SQLite is fine for development, consider PostgreSQL for production
3. **SSL**: PythonAnywhere provides free SSL certificates
4. **Backups**: Regularly backup your database and code
5. **Monitoring**: Set up monitoring for your production app

## 🚀 Next Steps

1. **Domain**: Consider using a custom domain
2. **Database**: Upgrade to PostgreSQL for better performance
3. **Caching**: Add Redis for session storage
4. **CDN**: Use a CDN for static files
5. **Monitoring**: Set up error tracking (Sentry)

## 📞 Support

If you encounter issues:
1. Check PythonAnywhere's documentation
2. Review Flask deployment guides
3. Check your application logs
4. Test locally first before deploying

Good luck with your deployment! 🎉
