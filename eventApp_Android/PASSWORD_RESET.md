# Password Reset System

This document describes the password reset system implemented in the EventApp application.

## Overview

The password reset system allows users to reset their passwords when they forget them. Users can request a password reset link via email, which they can use to set a new password.

## Features

- **Secure Password Reset**: Users can request password reset links via email
- **Time-Limited Tokens**: Reset tokens expire after 1 hour for security
- **Secure Token Generation**: Uses cryptographically secure tokens
- **Email Integration**: Professional HTML email templates
- **Security Best Practices**: Doesn't reveal if email exists in system

## Database Changes

The following fields were added to the `User` model:

- `password_reset_token`: Stores the password reset token (VARCHAR(100))
- `password_reset_sent_at`: Tracks when the password reset email was sent (DATETIME)

## User Flow

### Forgot Password Request

1. User clicks "Forgot your password?" on login page
2. User enters their email address
3. System generates secure reset token
4. System sends password reset email
5. User receives email with reset link

### Password Reset Process

1. User clicks reset link in email
2. System validates token and checks expiration
3. User enters new password (twice for confirmation)
4. System updates password and clears reset token
5. User can now log in with new password

## Routes

### `/forgot-password`
- **Method**: GET, POST
- **Purpose**: Request password reset
- **Behavior**:
  - GET: Shows form to enter email
  - POST: Sends password reset email (always shows success for security)

### `/reset-password/<token>`
- **Method**: GET, POST
- **Purpose**: Reset password with token
- **Behavior**:
  - GET: Shows password reset form
  - POST: Updates password and clears token

## Email Template

The password reset email includes:
- Professional HTML and text versions
- Clear call-to-action button
- Fallback text link
- Expiration notice (1 hour)
- Security information

## Security Features

- **Token Expiration**: Tokens expire after 1 hour
- **Secure Generation**: Uses `secrets.token_urlsafe(32)` for tokens
- **One-time Use**: Tokens are cleared after successful reset
- **Email Privacy**: Doesn't reveal if email exists in system
- **Password Validation**: Enforces minimum password requirements

## Configuration

Email settings are configured via environment variables (same as email verification):

```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

## Migration

To add password reset to existing installations:

1. Run the migration script:
   ```bash
   python migrate_password_reset.py
   ```

2. This will add the new database columns

## Testing

Run the test script to verify functionality:

```bash
python test_password_reset.py
```

## Security Considerations

### Token Security
- Tokens are cryptographically secure (32 bytes)
- Tokens expire after 1 hour
- Tokens are single-use (cleared after reset)

### Email Privacy
- System doesn't reveal if email exists
- Always shows "success" message for security
- Prevents email enumeration attacks

### Password Requirements
- Minimum 6 characters
- Password confirmation required
- Old password is immediately invalidated

## Troubleshooting

### Email Not Sending
- Check email configuration in environment variables
- Verify SMTP credentials
- Check firewall/network settings

### Token Issues
- Tokens expire after 1 hour
- Users can request new tokens via forgot password page
- Invalid tokens show appropriate error messages

### Database Issues
- Ensure migration script ran successfully
- Check database permissions
- Verify column additions

## Integration with Email Verification

The password reset system works alongside the email verification system:

- Users must have verified emails to use password reset
- Both systems use the same email configuration
- Both systems follow similar security patterns

## Future Enhancements

Potential improvements:
- Password reset reminders
- Multiple reset attempts tracking
- Admin panel for managing reset requests
- Integration with additional email service providers
- Custom email templates per organization
- Password strength requirements
- Account lockout after multiple failed attempts
