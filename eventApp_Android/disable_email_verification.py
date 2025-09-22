#!/usr/bin/env python3
"""
Temporary Email Verification Disable
This script temporarily disables email verification so you can use the app.
"""

import os
import shutil
from datetime import datetime

def backup_current_config():
    """Backup current configuration."""
    if os.path.exists('.env'):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f'.env.backup_{timestamp}'
        shutil.copy2('.env', backup_name)
        print(f"✅ Backed up current config to: {backup_name}")
        return backup_name
    return None

def create_no_email_config():
    """Create configuration without email verification."""
    config = """# EventApp Environment Configuration
# Temporary configuration without email verification

# Flask Configuration
SECRET_KEY=ff51f8a92aaa245c385f100331f943ed1dd42a2726d4546578ef5f787a980635
FLASK_ENV=development
DATABASE_URL=sqlite:///eventapp.db

# Email Configuration (Disabled)
MAIL_SERVER=
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=
MAIL_PASSWORD=

# App Configuration
APP_NAME=EventApp
"""
    
    with open('.env', 'w') as f:
        f.write(config)
    
    print("✅ Created configuration without email verification")

def update_app_for_no_email():
    """Update app.py to skip email verification."""
    print("📝 Updating app.py to skip email verification...")
    
    # Read current app.py
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace email verification logic
    old_code = """        # Send verification email
        try:
            send_verification_email(user)
            flash('Registration successful! Please check your email to verify your account.', 'success')
        except Exception as e:
            print(f"Failed to send verification email: {e}")
            flash('Registration successful, but failed to send verification email. Please check your email configuration or contact support.', 'warning')"""
    
    new_code = """        # Skip email verification for now
        user.email_verified = True
        flash('Registration successful! You can now log in.', 'success')"""
    
    if old_code in content:
        content = content.replace(old_code, new_code)
        
        # Write updated content
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Updated app.py to skip email verification")
        return True
    else:
        print("⚠️ Could not find email verification code to replace")
        return False

def main():
    print("=" * 60)
    print("🔧 Temporary Email Verification Disable")
    print("=" * 60)
    
    print("\n⚠️ This will temporarily disable email verification so you can use the app.")
    print("You can re-enable it later when email is working.")
    
    confirm = input("\nDo you want to proceed? (y/N): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Operation cancelled.")
        return False
    
    # Backup current config
    backup_file = backup_current_config()
    
    # Create no-email config
    create_no_email_config()
    
    # Update app.py
    success = update_app_for_no_email()
    
    if success:
        print("\n🎉 Email verification temporarily disabled!")
        print("\n📋 What this means:")
        print("• New users can register without email verification")
        print("• All users are automatically verified")
        print("• You can use the app normally")
        print("• Email features are disabled")
        
        print("\n🔄 To re-enable email verification later:")
        print(f"• Restore config: copy {backup_file} to .env")
        print("• Fix email configuration")
        print("• Restart the app")
        
        return True
    else:
        print("\n❌ Failed to update app.py")
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n✅ Setup complete! Restart your Flask app to apply changes.")
        print("📱 You can now register users without email verification.")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")
    
    print("=" * 60)
