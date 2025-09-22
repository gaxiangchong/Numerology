#!/usr/bin/env python3
"""
Quick Email Configuration Fix
This script helps you set up email with different providers if Outlook App Passwords are not available.
"""

import os

def create_gmail_config():
    """Create Gmail configuration."""
    print("📧 Setting up Gmail configuration...")
    print("\n📋 Gmail Setup Steps:")
    print("1. Go to: https://myaccount.google.com/security")
    print("2. Enable '2-Step Verification'")
    print("3. Go to 'App passwords'")
    print("4. Create a new app password for 'Mail'")
    print("5. Use the 16-character password below")
    
    email = input("\nEnter your Gmail address: ").strip()
    app_password = input("Enter your Gmail App Password (16 characters): ").strip()
    
    config = f"""# EventApp Environment Configuration
# Gmail Configuration

# Flask Configuration
SECRET_KEY=ff51f8a92aaa245c385f100331f943ed1dd42a2726d4546578ef5f787a980635
FLASK_ENV=development
DATABASE_URL=sqlite:///eventapp.db

# Gmail Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME={email}
MAIL_PASSWORD={app_password}

# App Configuration
APP_NAME=EventApp
"""
    
    with open('.env', 'w') as f:
        f.write(config)
    
    print("✅ Gmail configuration saved!")
    return True

def create_yahoo_config():
    """Create Yahoo configuration."""
    print("📧 Setting up Yahoo configuration...")
    print("\n📋 Yahoo Setup Steps:")
    print("1. Go to: https://login.yahoo.com/account/security")
    print("2. Enable 'Two-step verification'")
    print("3. Go to 'Generate app password'")
    print("4. Create a new app password")
    print("5. Use the generated password below")
    
    email = input("\nEnter your Yahoo email address: ").strip()
    app_password = input("Enter your Yahoo App Password: ").strip()
    
    config = f"""# EventApp Environment Configuration
# Yahoo Configuration

# Flask Configuration
SECRET_KEY=ff51f8a92aaa245c385f100331f943ed1dd42a2726d4546578ef5f787a980635
FLASK_ENV=development
DATABASE_URL=sqlite:///eventapp.db

# Yahoo Email Configuration
MAIL_SERVER=smtp.mail.yahoo.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME={email}
MAIL_PASSWORD={app_password}

# App Configuration
APP_NAME=EventApp
"""
    
    with open('.env', 'w') as f:
        f.write(config)
    
    print("✅ Yahoo configuration saved!")
    return True

def try_outlook_alternative():
    """Try alternative Outlook setup."""
    print("📧 Trying alternative Outlook setup...")
    print("\n📋 Alternative Outlook Steps:")
    print("1. Go to: https://account.microsoft.com/security")
    print("2. Click 'Security' in the left menu")
    print("3. Look for 'Advanced security options'")
    print("4. Enable 'Two-step verification' if not already enabled")
    print("5. Look for 'App passwords' section")
    print("6. Create a new app password")
    
    app_password = input("\nEnter your Outlook App Password (16 characters): ").strip()
    
    config = f"""# EventApp Environment Configuration
# Outlook Configuration (with App Password)

# Flask Configuration
SECRET_KEY=ff51f8a92aaa245c385f100331f943ed1dd42a2726d4546578ef5f787a980635
FLASK_ENV=development
DATABASE_URL=sqlite:///eventapp.db

# Outlook Email Configuration
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=noblequest.edu@outlook.com
MAIL_PASSWORD={app_password}

# App Configuration
APP_NAME=EventApp
"""
    
    with open('.env', 'w') as f:
        f.write(config)
    
    print("✅ Outlook configuration updated with App Password!")
    return True

def main():
    print("=" * 60)
    print("🔧 Quick Email Configuration Fix")
    print("=" * 60)
    print("\nSince you can't find the App Password option in Outlook,")
    print("let's try alternative solutions:")
    print("\n1. Try alternative Outlook setup (with App Password)")
    print("2. Switch to Gmail (easier setup)")
    print("3. Switch to Yahoo (easier setup)")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        return try_outlook_alternative()
    elif choice == "2":
        return create_gmail_config()
    elif choice == "3":
        return create_yahoo_config()
    elif choice == "4":
        print("👋 Goodbye!")
        return False
    else:
        print("❌ Invalid choice!")
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎉 Email configuration updated!")
        print("\n📋 Next steps:")
        print("1. Test the configuration: python test_email_config.py")
        print("2. Try registering a new user")
        print("3. Check if verification emails are sent")
    else:
        print("\n❌ Configuration not updated.")
    
    print("=" * 60)
