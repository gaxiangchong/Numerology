#!/usr/bin/env python3
"""
Test script to verify email verification is properly enabled and configured.
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_email_verification_setup():
    """Test email verification setup."""
    print("🔍 Testing Email Verification Setup...")
    print("=" * 50)
    
    try:
        from app import app, db, User, send_verification_email
        from dotenv import load_dotenv
        
        # Load environment variables
        load_dotenv()
        
        with app.app_context():
            # Test 1: Check User model default
            print("1. Testing User model email_verified default...")
            test_user = User()
            if test_user.email_verified == False:
                print("   ✅ User model default is correct (email_verified=False)")
            else:
                print(f"   ❌ User model default is incorrect (email_verified={test_user.email_verified})")
            
            # Test 2: Check email configuration
            print("\n2. Testing email configuration...")
            mail_server = app.config.get('MAIL_SERVER')
            mail_username = app.config.get('MAIL_USERNAME')
            mail_password = app.config.get('MAIL_PASSWORD')
            
            if mail_server and mail_username and mail_password:
                print(f"   ✅ Email server configured: {mail_server}")
                print(f"   ✅ Username configured: {mail_username}")
                print(f"   ✅ Password configured: {'*' * len(mail_password)}")
            else:
                print("   ❌ Email configuration incomplete:")
                print(f"      MAIL_SERVER: {mail_server}")
                print(f"      MAIL_USERNAME: {mail_username}")
                print(f"      MAIL_PASSWORD: {'Set' if mail_password else 'Not set'}")
            
            # Test 3: Check existing users
            print("\n3. Checking existing users...")
            users = User.query.all()
            verified_count = sum(1 for u in users if u.email_verified)
            unverified_count = len(users) - verified_count
            
            print(f"   Total users: {len(users)}")
            print(f"   Verified users: {verified_count}")
            print(f"   Unverified users: {unverified_count}")
            
            if unverified_count > 0:
                print("   ⚠️  Some users are unverified. They will need to verify their email.")
            
            # Test 4: Test email sending function
            print("\n4. Testing email sending function...")
            if mail_username and mail_password:
                print("   📧 Email configuration available - can test sending")
                print("   💡 To test email sending, create a test user and call send_verification_email()")
            else:
                print("   ❌ Cannot test email sending - configuration missing")
            
            print("\n" + "=" * 50)
            print("📋 Email Verification Status Summary:")
            print("=" * 50)
            
            if test_user.email_verified == False and mail_username and mail_password:
                print("✅ Email verification is PROPERLY ENABLED")
                print("✅ New users will need to verify their email")
                print("✅ Email configuration is available")
                print("\n🚀 Ready for production!")
            else:
                print("❌ Email verification setup needs attention:")
                if test_user.email_verified != False:
                    print("   - User model default needs to be False")
                if not mail_username or not mail_password:
                    print("   - Email configuration is missing")
                print("\n🔧 Please fix the issues above before deploying")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure you're running this from the eventapp directory")
    except Exception as e:
        print(f"❌ Error: {e}")

def create_sample_env():
    """Create a sample .env file for email configuration."""
    env_content = """# Email Configuration for EventApp
# Copy this file to .env and update with your email settings

# Gmail Configuration (Recommended)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Outlook Configuration (Alternative)
# MAIL_SERVER=smtp-mail.outlook.com
# MAIL_PORT=587
# MAIL_USE_TLS=True
# MAIL_USERNAME=your-email@outlook.com
# MAIL_PASSWORD=your-app-password

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

# Stripe Configuration (Optional)
# STRIPE_PUBLISHABLE_KEY=pk_test_...
# STRIPE_SECRET_KEY=sk_test_...
# STRIPE_WEBHOOK_SECRET=whsec_...
"""
    
    env_file = os.path.join(os.path.dirname(__file__), '.env.example')
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"\n📄 Created sample .env file: {env_file}")
    print("   Copy this to .env and update with your email settings")

if __name__ == "__main__":
    test_email_verification_setup()
    create_sample_env()
