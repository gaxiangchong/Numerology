#!/usr/bin/env python3
"""
Migration script to handle existing users when email verification is re-enabled.
This script provides options for managing existing users who were created when
email verification was disabled.
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def migrate_existing_users():
    """Handle existing users for email verification."""
    print("🔄 Email Verification Migration for Existing Users")
    print("=" * 60)
    
    # Check if we can import Flask modules
    try:
        import flask
        import flask_sqlalchemy
        import flask_login
    except ImportError as e:
        print(f"❌ Flask modules not available: {e}")
        print("   This script requires Flask to be installed and available.")
        print("   You can run this script on PythonAnywhere or in your virtual environment.")
        print("\n📋 For now, you can manually handle existing users:")
        print("   1. Auto-verify all existing users (recommended)")
        print("   2. Send verification emails to existing users")
        print("   3. Leave existing users as-is (they'll need to verify manually)")
        return
    
    try:
        from app import app, db, User, send_verification_email
        
        with app.app_context():
            # Get all users
            users = User.query.all()
            print(f"Found {len(users)} users in the database")
            
            if not users:
                print("No users found. Nothing to migrate.")
                return
            
            # Analyze users
            verified_users = [u for u in users if u.email_verified]
            unverified_users = [u for u in users if not u.email_verified]
            
            print(f"\n📊 Current Status:")
            print(f"   Verified users: {len(verified_users)}")
            print(f"   Unverified users: {len(unverified_users)}")
            
            if len(unverified_users) == 0:
                print("\n✅ All users are already verified. No migration needed.")
                return
            
            print(f"\n⚠️  Found {len(unverified_users)} unverified users:")
            for user in unverified_users:
                print(f"   - {user.username} ({user.email}) - Created: {user.created_at}")
            
            # Provide options
            print(f"\n🔧 Migration Options:")
            print("1. Auto-verify all existing users (recommended for existing users)")
            print("2. Send verification emails to all unverified users")
            print("3. Leave unverified users as-is (they'll need to verify manually)")
            print("4. Show detailed user information")
            
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                auto_verify_all_users(unverified_users)
            elif choice == "2":
                send_verification_emails(unverified_users)
            elif choice == "3":
                print("✅ Leaving unverified users as-is. They will need to verify manually.")
            elif choice == "4":
                show_detailed_user_info(users)
            else:
                print("❌ Invalid choice. Exiting.")
                
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure you're running this from the eventapp directory")
    except Exception as e:
        print(f"❌ Error: {e}")

def auto_verify_all_users(unverified_users):
    """Auto-verify all existing users."""
    print(f"\n🔄 Auto-verifying {len(unverified_users)} users...")
    
    try:
        from app import app, db, User
        
        with app.app_context():
            for user in unverified_users:
                user.email_verified = True
                user.email_verification_token = None
                user.email_verification_sent_at = None
                print(f"   ✅ Verified: {user.username} ({user.email})")
            
            db.session.commit()
            print(f"\n✅ Successfully verified {len(unverified_users)} users!")
            print("   These users can now log in without email verification.")
            
    except Exception as e:
        print(f"❌ Error during auto-verification: {e}")

def send_verification_emails(unverified_users):
    """Send verification emails to unverified users."""
    print(f"\n📧 Sending verification emails to {len(unverified_users)} users...")
    
    try:
        from app import app, db, User, send_verification_email
        
        with app.app_context():
            success_count = 0
            failed_count = 0
            
            for user in unverified_users:
                try:
                    if send_verification_email(user):
                        success_count += 1
                        print(f"   ✅ Sent to: {user.username} ({user.email})")
                    else:
                        failed_count += 1
                        print(f"   ❌ Failed: {user.username} ({user.email})")
                except Exception as e:
                    failed_count += 1
                    print(f"   ❌ Error for {user.username}: {e}")
            
            print(f"\n📊 Email sending results:")
            print(f"   ✅ Successfully sent: {success_count}")
            print(f"   ❌ Failed to send: {failed_count}")
            
            if failed_count > 0:
                print("\n⚠️  Some emails failed to send. Check your email configuration.")
            
    except Exception as e:
        print(f"❌ Error during email sending: {e}")

def show_detailed_user_info(users):
    """Show detailed information about all users."""
    print(f"\n📋 Detailed User Information:")
    print("=" * 80)
    
    for user in users:
        print(f"\n👤 User: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Verified: {'✅ Yes' if user.email_verified else '❌ No'}")
        print(f"   Admin: {'✅ Yes' if user.is_admin else '❌ No'}")
        print(f"   Created: {user.created_at}")
        print(f"   Membership Type: {user.membership_type}")
        print(f"   Membership Grade: {user.membership_grade}")
        
        if user.email_verification_token:
            print(f"   Verification Token: {user.email_verification_token[:10]}...")
        if user.email_verification_sent_at:
            print(f"   Last Verification Sent: {user.email_verification_sent_at}")

def create_email_config_guide():
    """Create a guide for email configuration."""
    guide_content = """
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
"""
    
    guide_file = os.path.join(os.path.dirname(__file__), 'EMAIL_CONFIG_GUIDE.md')
    with open(guide_file, 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print(f"\n📖 Created email configuration guide: {guide_file}")

if __name__ == "__main__":
    migrate_existing_users()
    create_email_config_guide()
