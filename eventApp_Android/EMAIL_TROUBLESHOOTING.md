# Email Troubleshooting Guide

This guide helps you resolve email sending issues in EventApp.

## Common Error: "Failed to send password reset email"

This error occurs when the email configuration is not properly set up. Follow these steps to fix it:

## Step 1: Check Email Configuration

### 1.1 Create .env File
Create a `.env` file in the `eventapp` directory with the following content:

```env
# Flask Configuration
SECRET_KEY=your-very-secure-secret-key-here
FLASK_ENV=development
DATABASE_URL=sqlite:///eventapp.db

# Email Configuration (Required for password reset and email verification)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# App Configuration
APP_NAME=EventApp
ADMIN_EMAIL=admin@yourapp.com
```

### 1.2 Test Email Configuration
Run the email configuration test:
```bash
python test_email_config.py
```

## Step 2: Gmail Setup (Most Common)

### 2.1 Enable 2-Factor Authentication
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable 2-Step Verification if not already enabled

### 2.2 Generate App Password
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Click on "2-Step Verification"
3. Scroll down to "App passwords"
4. Click "App passwords"
5. Select "Mail" as the app
6. Copy the generated 16-character password

### 2.3 Update .env File
```env
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-character-app-password
```

## Step 3: Other Email Providers

### Outlook/Hotmail
```env
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@outlook.com
MAIL_PASSWORD=your-password
```

### Yahoo Mail
```env
MAIL_SERVER=smtp.mail.yahoo.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@yahoo.com
MAIL_PASSWORD=your-app-password
```

### Custom SMTP
Contact your email provider for SMTP settings.

## Step 4: Common Issues and Solutions

### Issue 1: "SMTP Authentication failed"
**Solution:**
- Check your email and password
- For Gmail, use App Password, not regular password
- Ensure 2-factor authentication is enabled

### Issue 2: "Connection refused"
**Solution:**
- Check your internet connection
- Verify SMTP server and port
- Check firewall settings

### Issue 3: "Recipient refused"
**Solution:**
- Check if the email address is valid
- Some email providers block automated emails

### Issue 4: "Email not configured"
**Solution:**
- Ensure .env file exists
- Check that MAIL_USERNAME and MAIL_PASSWORD are set
- Restart the application after updating .env

## Step 5: Testing

### 5.1 Test Email Configuration
```bash
python test_email_config.py
```

### 5.2 Test Password Reset
1. Go to login page
2. Click "Forgot your password?"
3. Enter your email
4. Check for success message
5. Check your email inbox

### 5.3 Check Application Logs
Look for detailed error messages in the console output when running the app.

## Step 6: Development vs Production

### Development (Local Testing)
- Use your personal email for testing
- Gmail App Passwords work well
- Check spam folder for test emails

### Production (PythonAnywhere)
- Use a dedicated email service
- Consider using SendGrid, Mailgun, or similar
- Update .env file on production server

## Step 7: Alternative Email Services

If Gmail doesn't work, consider these alternatives:

### SendGrid (Recommended for Production)
1. Sign up at [SendGrid](https://sendgrid.com/)
2. Get API key
3. Update .env:
```env
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=apikey
MAIL_PASSWORD=your-sendgrid-api-key
```

### Mailgun
1. Sign up at [Mailgun](https://www.mailgun.com/)
2. Get SMTP credentials
3. Update .env with Mailgun settings

## Step 8: Debugging Tips

### Enable Debug Logging
Add this to your .env file:
```env
FLASK_ENV=development
```

### Check Console Output
When running the app, look for detailed error messages:
```
❌ Email not configured. Missing MAIL_USERNAME or MAIL_PASSWORD
📧 Attempting to send email to user@example.com...
❌ SMTP Authentication failed: (535, '5.7.8 Username and Password not accepted')
```

### Test with Simple Email
Try sending a simple test email first before testing the full application.

## Still Having Issues?

1. **Check the console output** for detailed error messages
2. **Verify your .env file** is in the correct location
3. **Test with a different email provider**
4. **Check your internet connection**
5. **Restart the application** after making changes

## Security Notes

- Never commit your .env file to version control
- Use App Passwords instead of regular passwords
- Keep your email credentials secure
- Consider using environment variables in production
