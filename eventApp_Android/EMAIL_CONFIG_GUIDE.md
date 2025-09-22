
# Email Configuration Guide for EventApp

## Quick Setup for Gmail

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate an App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a password for "Mail"
3. **Create .env file** with these settings:

```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-character-app-password
ADMIN_EMAIL=your-email@gmail.com
```

## Quick Setup for Outlook

1. **Enable 2-Factor Authentication** on your Outlook account
2. **Generate an App Password**:
   - Go to Microsoft Account security settings
   - Advanced security options → App passwords
   - Generate a password for "Mail"
3. **Create .env file** with these settings:

```
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@outlook.com
MAIL_PASSWORD=your-app-password
ADMIN_EMAIL=your-email@outlook.com
```

## Testing Email Configuration

Run this command to test your email setup:
```bash
python test_email_verification_enabled.py
```

## Troubleshooting

- **Authentication failed**: Check your app password
- **Connection timeout**: Check your internet connection
- **SMTP server error**: Verify server settings
- **Emails not received**: Check spam folder

## Important Notes

- App passwords are different from your regular password
- Never share your app password
- If you change your main password, you may need to regenerate the app password
