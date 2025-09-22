#!/usr/bin/env python3
"""
Quick Outlook setup - just run this script and follow the prompts.
"""

import os
import secrets

def quick_outlook_setup():
    print("🚀 Quick Outlook Setup for EventApp")
    print("=" * 35)
    
    email = input("Your Outlook email: ").strip()
    password = input("Your Outlook password: ").strip()
    
    if not email or not password:
        print("❌ Email and password are required!")
        return
    
    secret_key = secrets.token_hex(32)
    
    env_content = f"""SECRET_KEY={secret_key}
FLASK_ENV=development
DATABASE_URL=sqlite:///eventapp.db
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME={email}
MAIL_PASSWORD={password}
APP_NAME=EventApp
ADMIN_EMAIL={email}"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Setup complete! Run: python test_email_config.py")

if __name__ == '__main__':
    quick_outlook_setup()
