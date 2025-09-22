# Email Verification System

This document describes the email verification system implemented in the EventApp application.

## Overview

The email verification system ensures that users must verify their email addresses before they can use their accounts. This helps prevent spam registrations and ensures that users have access to the email addresses they provide.

## Features

- **Email Verification Required**: Users must click a verification link in their email before they can log in
- **Secure Tokens**: Uses cryptographically secure tokens that expire after 24 hours
- **Resend Functionality**: Users can request new verification emails if needed
- **Automatic Redirects**: Unverified users are automatically redirected to verification pages
- **Existing User Support**: Existing users are grandfathered in with verified emails

## Database Changes

The following fields were added to the `User` model:

- `email_verification_token`: Stores the verification token (VARCHAR(100))
- `email_verification_sent_at`: Tracks when the verification email was sent (DATETIME)

## User Flow

### New User Registration

1. User fills out registration form
2. System creates user account with `email_verified = False`
3. System generates verification token and sends email
4. User receives email with verification link
5. User clicks link to verify email
6. System sets `email_verified = True` and clears token
7. User can now log in and use the application

### Login Process

1. User attempts to log in
2. System checks if email is verified
3. If not verified, user is redirected to resend verification page
4. If verified, user is logged in normally

### Middleware Protection

- All authenticated users with unverified emails are redirected to verification page
- Exceptions: verification routes, logout, and resend verification

## Routes

### `/verify-email/<token>`
- **Method**: GET
- **Purpose**: Verify email with token
- **Behavior**: 
  - Validates token
  - Checks expiration (24 hours)
  - Sets email as verified
  - Redirects to login

### `/resend-verification`
- **Method**: GET, POST
- **Purpose**: Resend verification email
- **Behavior**:
  - GET: Shows form to enter email
  - POST: Sends new verification email

## Email Template

The verification email includes:
- Professional HTML and text versions
- Clear call-to-action button
- Fallback text link
- Expiration notice (24 hours)
- Security information

## Security Features

- **Token Expiration**: Tokens expire after 24 hours
- **Secure Generation**: Uses `secrets.token_urlsafe(32)` for tokens
- **One-time Use**: Tokens are cleared after successful verification
- **Email Validation**: Proper email format validation

## Configuration

Email settings are configured via environment variables:

```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

## Migration

To add email verification to existing installations:

1. Run the migration script:
   ```bash
   python migrate_email_verification.py
   ```

2. This will:
   - Add new database columns
   - Set existing users as verified (grandfathering)

## Testing

Run the test script to verify functionality:

```bash
python test_email_verification.py
```

## Troubleshooting

### Email Not Sending
- Check email configuration in environment variables
- Verify SMTP credentials
- Check firewall/network settings

### Token Issues
- Tokens expire after 24 hours
- Users can request new tokens via resend page
- Invalid tokens show appropriate error messages

### Database Issues
- Ensure migration script ran successfully
- Check database permissions
- Verify column additions

## Future Enhancements

Potential improvements:
- Email verification reminders
- Multiple verification attempts tracking
- Admin panel for managing verification status
- Integration with email service providers (SendGrid, etc.)
- Custom email templates per organization
