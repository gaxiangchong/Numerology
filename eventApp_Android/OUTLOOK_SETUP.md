# Outlook Email Setup for EventApp

This guide helps you configure Outlook/Hotmail email for password reset and email verification.

## Quick Setup for Outlook

### Step 1: Create .env File
Create a `.env` file in the `eventapp` directory with the following content:

```env
# EventApp Environment Configuration

# Flask Configuration
SECRET_KEY=your-very-secure-secret-key-here
FLASK_ENV=development
DATABASE_URL=sqlite:///eventapp.db

# Outlook Email Configuration
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@outlook.com
MAIL_PASSWORD=your-outlook-password

# App Configuration
APP_NAME=EventApp
ADMIN_EMAIL=your-email@outlook.com
```

### Step 2: Replace Placeholder Values

1. **SECRET_KEY**: Generate a secure key:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

2. **MAIL_USERNAME**: Your full Outlook email address
   - Example: `john.doe@outlook.com`
   - Example: `jane.smith@hotmail.com`

3. **MAIL_PASSWORD**: Your Outlook account password
   - Use your regular Outlook password
   - If you have 2FA enabled, you may need an App Password

### Step 3: Test Configuration
Run the email test:
```bash
python test_email_config.py
```

## Outlook-Specific Settings

### Supported Outlook Domains
- `@outlook.com`
- `@hotmail.com`
- `@live.com`
- `@msn.com`

### SMTP Settings
- **Server**: `smtp-mail.outlook.com`
- **Port**: `587`
- **Encryption**: `TLS`
- **Authentication**: Required

## Troubleshooting Outlook Issues

### Issue 1: Authentication Failed
**Symptoms**: "SMTP Authentication failed" error
**Solutions**:
1. Check your email and password
2. Ensure you're using your full email address
3. Try logging into Outlook.com with the same credentials

### Issue 2: 2-Factor Authentication
If you have 2FA enabled on your Outlook account:
1. Go to [Microsoft Account Security](https://account.microsoft.com/security)
2. Click "Advanced security options"
3. Create an App Password
4. Use the App Password instead of your regular password

### Issue 3: Connection Issues
**Symptoms**: "Connection refused" or timeout errors
**Solutions**:
1. Check your internet connection
2. Try a different network
3. Check if your firewall blocks port 587

## Alternative Outlook Settings

If the standard settings don't work, try these alternatives:

### Alternative 1: Different Port
```env
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=25
MAIL_USE_TLS=True
```

### Alternative 2: SSL Instead of TLS
```env
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=465
MAIL_USE_TLS=False
MAIL_USE_SSL=True
```

## Testing Your Setup

### 1. Run Email Configuration Test
```bash
python test_email_config.py
```

### 2. Test Password Reset
1. Start your application: `python app.py`
2. Go to login page
3. Click "Forgot your password?"
4. Enter your Outlook email
5. Check your Outlook inbox

### 3. Test Email Verification
1. Try registering a new account
2. Check if verification email is received
3. Click the verification link

## Security Notes

- Never share your email credentials
- Use strong passwords
- Consider using App Passwords for better security
- Keep your .env file secure and never commit it to version control

## Common Outlook Issues

### "Less Secure App Access"
Outlook may block "less secure apps". To fix:
1. Go to [Microsoft Account Security](https://account.microsoft.com/security)
2. Enable "Less secure app access" (if available)
3. Or use App Passwords instead

### "Account Locked"
If your account gets locked:
1. Wait 24 hours
2. Try logging into Outlook.com first
3. Use App Passwords for better security

## Need Help?

If you're still having issues:
1. Check the console output for detailed error messages
2. Try the alternative SMTP settings above
3. Test with a different email provider
4. Check your Outlook account settings
