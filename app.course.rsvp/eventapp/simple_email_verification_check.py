#!/usr/bin/env python3
"""
Simple script to check email verification status without requiring Flask imports.
This can be run in any environment to verify the email verification setup.
"""

import os
import sys

def check_email_verification_files():
    """Check if email verification files are properly configured."""
    print("🔍 Checking Email Verification Files...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ app.py not found. Make sure you're in the eventapp directory.")
        return False
    
    # Check app.py for email verification settings
    print("1. Checking app.py for email verification settings...")
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for key email verification components
        checks = [
            ('email_verified = db.Column(db.Boolean, default=False)', 'User model default'),
            ('if current_user.is_authenticated and not current_user.email_verified:', 'Before request check'),
            ('user.email_verified = False', 'Registration sets unverified'),
            ('send_verification_email(user)', 'Sends verification email'),
            ('if not user.email_verified:', 'Login checks verification'),
        ]
        
        all_good = True
        for check_text, description in checks:
            if check_text in content:
                print(f"   ✅ {description}")
            else:
                print(f"   ❌ {description} - NOT FOUND")
                all_good = False
        
        return all_good
        
    except Exception as e:
        print(f"   ❌ Error reading app.py: {e}")
        return False

def check_templates():
    """Check if templates are properly configured."""
    print("\n2. Checking templates...")
    
    template_checks = [
        ('templates/register.html', 'Registration template'),
        ('templates/resend_verification.html', 'Resend verification template'),
        ('templates/verify.html', 'Verify email template'),
    ]
    
    all_good = True
    for template_path, description in template_checks:
        if os.path.exists(template_path):
            print(f"   ✅ {description}")
        else:
            print(f"   ❌ {description} - NOT FOUND")
            all_good = False
    
    return all_good

def check_env_configuration():
    """Check for email configuration files."""
    print("\n3. Checking email configuration...")
    
    env_files = ['.env', '.env.example']
    found_env = False
    
    for env_file in env_files:
        if os.path.exists(env_file):
            print(f"   ✅ {env_file} found")
            found_env = True
            
            # Check if it has email settings
            try:
                with open(env_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if 'MAIL_SERVER' in content and 'MAIL_USERNAME' in content:
                    print(f"   ✅ {env_file} contains email settings")
                else:
                    print(f"   ⚠️  {env_file} missing email settings")
            except Exception as e:
                print(f"   ❌ Error reading {env_file}: {e}")
        else:
            print(f"   ❌ {env_file} not found")
    
    if not found_env:
        print("   ⚠️  No .env files found. You'll need to create one for email configuration.")
    
    return found_env

def create_simple_env_example():
    """Create a simple .env.example file."""
    env_content = """# Email Configuration for EventApp
# Copy this file to .env and update with your email settings

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
"""
    
    try:
        with open('.env.example', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("\n📄 Created .env.example file")
        return True
    except Exception as e:
        print(f"\n❌ Error creating .env.example: {e}")
        return False

def main():
    """Main function to run all checks."""
    print("🚀 Email Verification Setup Checker")
    print("=" * 50)
    
    # Run all checks
    app_check = check_email_verification_files()
    template_check = check_templates()
    env_check = check_env_configuration()
    
    # Create .env.example if it doesn't exist
    if not os.path.exists('.env.example'):
        create_simple_env_example()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 SUMMARY")
    print("=" * 50)
    
    if app_check and template_check:
        print("✅ Email verification is PROPERLY ENABLED in the code")
        print("✅ All required templates are present")
        
        if env_check:
            print("✅ Email configuration files found")
            print("\n🚀 Ready for deployment!")
        else:
            print("⚠️  Email configuration needed")
            print("   Create a .env file with your email settings")
            print("   Use .env.example as a template")
    else:
        print("❌ Email verification setup needs attention")
        if not app_check:
            print("   - Code changes needed in app.py")
        if not template_check:
            print("   - Template files missing")
    
    print("\n📖 Next steps:")
    print("1. Set up email configuration in .env file")
    print("2. Test email sending functionality")
    print("3. Deploy to PythonAnywhere")
    print("4. Run migration script for existing users")

if __name__ == "__main__":
    main()
