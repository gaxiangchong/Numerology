# EventApp Deployment Guide for PythonAnywhere

## Prerequisites
- PythonAnywhere account (free or paid)
- Basic understanding of Flask applications

## Step 1: Prepare Your Application

1. **Create a new directory structure on PythonAnywhere:**
   ```
   /home/yourusername/eventapp/
   ├── app.py
   ├── requirements.txt
   ├── templates/
   ├── static/
   └── .env (create this file)
   ```

2. **Upload your files** to PythonAnywhere using the Files tab or Git.

## Step 2: Configure Environment Variables

Create a `.env` file in your project directory with the following content:

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

**Important Security Notes:**
- Generate a strong SECRET_KEY (you can use: `python -c "import secrets; print(secrets.token_hex(32))"`)
- For Gmail, use an App Password, not your regular password
- Never commit the .env file to version control

## Step 3: Install Dependencies

1. Open a Bash console on PythonAnywhere
2. Navigate to your project directory:
   ```bash
   cd /home/yourusername/eventapp
   ```
3. Create a virtual environment:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 eventapp
   ```
4. Activate the virtual environment:
   ```bash
   workon eventapp
   ```
5. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

## Step 4: Initialize Database

1. In the Bash console, run:
   ```bash
   python app.py
   ```
2. This will create the SQLite database file
3. Press Ctrl+C to stop the server

## Step 5: Configure Web App

1. Go to the **Web** tab in PythonAnywhere
2. Click **Add a new web app**
3. Choose **Flask** and **Python 3.10**
4. Set the path to: `/home/yourusername/eventapp/app.py`
5. Set the working directory to: `/home/yourusername/eventapp`

## Step 6: Configure WSGI File

Edit the WSGI file (usually `/var/www/yourusername_pythonanywhere_com_wsgi.py`) to:

```python
import sys
import os

# Add your project directory to the Python path
path = '/home/yourusername/eventapp'
if path not in sys.path:
    sys.path.append(path)

# Import your Flask app
from app import app as application

if __name__ == "__main__":
    application.run()
```

## Step 7: Create Admin User

1. Open a Bash console
2. Navigate to your project directory
3. Run Python:
   ```bash
   python
   ```
4. Execute the following commands:
   ```python
   from app import app, db, User
   with app.app_context():
       # Create admin user
       admin = User(username='admin', email='admin@yourapp.com', is_admin=True)
       admin.set_password('your-admin-password')
       db.session.add(admin)
       db.session.commit()
       print("Admin user created!")
   ```

## Step 8: Configure Static Files

In the Web tab, add these static file mappings:
- URL: `/static/`
- Directory: `/home/yourusername/eventapp/static/`

## Step 9: Reload Web App

Click the **Reload** button in the Web tab to apply all changes.

## Step 10: Test Your Application

1. Visit your PythonAnywhere URL
2. Register a new user account
3. Create an event (if you're an admin)
4. Test RSVP functionality
5. Test QR code generation and verification

## Troubleshooting

### Common Issues:

1. **Import Errors**: Make sure all dependencies are installed in your virtual environment
2. **Database Issues**: Ensure the database file has proper permissions
3. **Email Not Working**: Check your email configuration and app passwords
4. **Static Files Not Loading**: Verify static file mappings in the Web tab

### Logs:
- Check the **Error log** in the Web tab for application errors
- Check the **Server log** for server-related issues

## Security Considerations

1. **Change Default Secret Key**: Always use a strong, unique secret key
2. **Use HTTPS**: PythonAnywhere provides HTTPS by default
3. **Email Security**: Use app-specific passwords for email
4. **Database Security**: SQLite files should have restricted permissions
5. **Input Validation**: The app includes basic validation, but consider additional security measures for production

## Performance Optimization

1. **Database Indexing**: Add indexes for frequently queried fields
2. **Caching**: Consider implementing Redis for session storage
3. **Static Files**: Use a CDN for static assets in production
4. **Database Connection Pooling**: For high-traffic applications

## Backup Strategy

1. **Database Backup**: Regularly backup your SQLite database file
2. **Code Backup**: Use Git for version control
3. **Configuration Backup**: Keep a copy of your .env file (without sensitive data)

## Monitoring

1. **Error Tracking**: Monitor the error logs regularly
2. **Performance**: Use PythonAnywhere's monitoring tools
3. **User Activity**: Implement logging for important user actions

## Scaling Considerations

For high-traffic applications:
1. Upgrade to a paid PythonAnywhere plan
2. Consider migrating to PostgreSQL
3. Implement proper caching strategies
4. Use a dedicated email service (SendGrid, Mailgun)

## Support

- PythonAnywhere Documentation: https://help.pythonanywhere.com/
- Flask Documentation: https://flask.palletsprojects.com/
- Community Forums: PythonAnywhere and Flask communities
