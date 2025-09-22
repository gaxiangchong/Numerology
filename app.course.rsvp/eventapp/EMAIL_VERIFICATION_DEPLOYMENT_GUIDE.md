# Email Verification Deployment Guide

## ✅ Status: Email Verification is ENABLED

Email verification has been successfully re-enabled in your EventApp. Here's what you need to know:

## 🔧 What Was Changed

### Code Changes Made:
- ✅ **User Model**: `email_verified` default changed from `True` to `False`
- ✅ **Registration Flow**: New users must verify email before logging in
- ✅ **Login Protection**: Unverified users cannot log in
- ✅ **Email Sending**: Verification emails are sent automatically
- ✅ **Route Protection**: Unverified users redirected to verification page
- ✅ **Templates Updated**: Registration form shows verification requirement

### Files Modified:
- `app.py` - Core email verification logic
- `templates/register.html` - Updated registration message

### New Files Created:
- `test_email_verification_enabled.py` - Test email verification setup
- `migrate_existing_users_email_verification.py` - Handle existing users
- `simple_email_verification_check.py` - Simple verification checker
- `.env.example` - Sample email configuration
- `EMAIL_CONFIG_GUIDE.md` - Detailed email setup guide

## 🚀 Deployment Steps

### 1. Set Up Email Configuration

Create a `.env` file with your email settings:

```env
# Gmail Configuration (Recommended)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Admin email for notifications
ADMIN_EMAIL=admin@yourdomain.com

# Application settings
SECRET_KEY=your-secret-key-here
SERVER_NAME=your-domain.com
APPLICATION_ROOT=/
PREFERRED_URL_SCHEME=https

# Database
DATABASE_URL=sqlite:///eventapp.db

# Superuser password for admin operations
SUPERUSER_PASSWORD=your-superuser-password
```

### 2. Handle Existing Users

When you deploy to PythonAnywhere, run the migration script:

```bash
python migrate_existing_users_email_verification.py
```

**Options for existing users:**
1. **Auto-verify all existing users** (recommended)
2. **Send verification emails to existing users**
3. **Leave unverified** (they'll need to verify manually)

### 3. Test Email Verification

Run the test script to verify everything is working:

```bash
python simple_email_verification_check.py
```

### 4. Deploy to PythonAnywhere

1. **Push changes to Git**:
   ```bash
   git add .
   git commit -m "Enable email verification system"
   git push origin main
   ```

2. **Pull on PythonAnywhere**:
   ```bash
   git pull origin main
   ```

3. **Set up email configuration** in PythonAnywhere console

4. **Run migration script** for existing users

5. **Reload your web app**

## 📧 Email Setup Requirements

### For Gmail:
1. Enable 2-Factor Authentication
2. Generate App Password
3. Use App Password in `.env` file

### For Outlook:
1. Enable 2-Factor Authentication  
2. Generate App Password
3. Use App Password in `.env` file

## 🔍 How It Works Now

### New User Registration:
1. User fills registration form
2. Account created with `email_verified = False`
3. Verification email sent automatically
4. User clicks verification link
5. Account activated, user can log in

### Existing Users:
- Run migration script to handle them
- Choose to auto-verify or send verification emails

### Login Process:
1. User enters credentials
2. System checks if email is verified
3. If not verified → redirect to verification page
4. If verified → allow login

## ⚠️ Important Notes

- **New users MUST verify email** before they can log in
- **Existing users** need to be handled via migration script
- **Email configuration** is required for verification emails
- **App passwords** are different from regular passwords
- **Check spam folder** for verification emails

## 🛠️ Troubleshooting

### If emails aren't sending:
1. Check `.env` file configuration
2. Verify app password is correct
3. Test email configuration
4. Check PythonAnywhere email limits

### If users can't log in:
1. Check if email is verified
2. Run migration script for existing users
3. Check email configuration

### If verification links don't work:
1. Check `SERVER_NAME` in `.env`
2. Verify `PREFERRED_URL_SCHEME` is correct
3. Check if links are expired (24 hours)

## 📞 Support

If you encounter issues:
1. Run `python simple_email_verification_check.py` to diagnose
2. Check the `EMAIL_CONFIG_GUIDE.md` for detailed setup
3. Verify your email configuration
4. Test with a new user registration

---

**Email verification is now fully enabled and ready for production use!** 🎉
