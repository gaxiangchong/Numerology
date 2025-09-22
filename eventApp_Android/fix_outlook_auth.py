#!/usr/bin/env python3
"""
Fix Outlook authentication issue.

The error "basic authentication is disabled" means you need to use an App Password.
"""

import os

def fix_outlook_auth():
    print("🔧 Fixing Outlook Authentication Issue")
    print("=" * 40)
    print()
    
    print("❌ Error: 'basic authentication is disabled'")
    print("✅ Solution: Use an App Password instead of your regular password")
    print()
    
    print("📋 Steps to create an App Password:")
    print("1. Go to: https://account.microsoft.com/security")
    print("2. Sign in with your Outlook account")
    print("3. Click 'Advanced security options'")
    print("4. Under 'App passwords', click 'Create a new app password'")
    print("5. Give it a name like 'EventApp'")
    print("6. Copy the generated 16-character password")
    print()
    
    print("🔄 Alternative method:")
    print("1. Go to: https://myaccount.microsoft.com/")
    print("2. Click 'Security'")
    print("3. Click 'Advanced security options'")
    print("4. Click 'Create a new app password'")
    print()
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("❌ No .env file found. Please run setup_outlook.py first.")
        return
    
    # Read current .env
    with open('.env', 'r') as f:
        content = f.read()
    
    print("📝 Current .env file found.")
    print("After creating your App Password:")
    print("1. Run: python setup_outlook.py")
    print("2. Use your App Password (not regular password)")
    print("3. Or manually edit .env file and replace MAIL_PASSWORD")
    print()
    
    # Show current email
    for line in content.split('\n'):
        if line.startswith('MAIL_USERNAME='):
            email = line.split('=', 1)[1]
            print(f"📧 Your email: {email}")
            break
    
    print()
    print("💡 Quick fix - Update your .env file:")
    print("Replace the MAIL_PASSWORD line with:")
    print("MAIL_PASSWORD=your-16-character-app-password")
    print()
    print("Then test again with: python test_email_config.py")

if __name__ == '__main__':
    fix_outlook_auth()
