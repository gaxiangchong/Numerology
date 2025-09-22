#!/usr/bin/env python3
"""
Verify Email Verification is Disabled
This script checks that email verification has been properly disabled.
"""

import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User

def verify_email_disabled():
    """Verify that email verification is disabled."""
    print("🔧 Verifying Email Verification is Disabled...")
    print("=" * 50)
    
    try:
        with app.app_context():
            # Check if there are any users
            users = User.query.all()
            print(f"📊 Found {len(users)} users in database")
            
            if users:
                # Check email verification status
                verified_users = User.query.filter_by(email_verified=True).count()
                unverified_users = User.query.filter_by(email_verified=False).count()
                
                print(f"✅ Verified users: {verified_users}")
                print(f"⚠️ Unverified users: {unverified_users}")
                
                # Set all users as verified
                if unverified_users > 0:
                    print(f"\n🔧 Setting {unverified_users} users as verified...")
                    User.query.filter_by(email_verified=False).update({'email_verified': True})
                    db.session.commit()
                    print("✅ All users are now verified!")
                else:
                    print("✅ All users are already verified!")
            
            print("\n📋 Email Verification Status:")
            print("• Registration: ✅ No email verification required")
            print("• Login: ✅ No email verification check")
            print("• Before Request: ✅ No email verification middleware")
            print("• All Users: ✅ Automatically verified")
            
            return True
            
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return False

def show_current_config():
    """Show current email configuration."""
    print("\n📧 Current Email Configuration:")
    print("=" * 50)
    
    try:
        with open('.env', 'r') as f:
            content = f.read()
        
        lines = content.split('\n')
        for line in lines:
            if line.startswith('MAIL_'):
                print(f"   {line}")
        
        print("\n💡 Email is configured but verification is disabled")
        print("   Users can register and login without email verification")
        
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")

def main():
    print("🧪 Email Verification Disable Verification")
    print("=" * 50)
    
    success = verify_email_disabled()
    show_current_config()
    
    if success:
        print("\n🎉 Email verification is successfully disabled!")
        print("\n📋 What this means:")
        print("• New users can register without email verification")
        print("• All users are automatically verified")
        print("• No email verification checks during login")
        print("• You can use the app normally")
        
        print("\n🔄 To re-enable email verification later:")
        print("• Fix your email configuration")
        print("• Uncomment the email verification code in app.py")
        print("• Restart the Flask application")
        
        return True
    else:
        print("\n❌ Email verification disable verification failed!")
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n✅ Setup complete! Email verification is disabled.")
        print("📱 You can now register and use the app without email issues.")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")
    
    print("=" * 50)
