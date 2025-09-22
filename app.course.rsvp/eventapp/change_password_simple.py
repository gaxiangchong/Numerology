#!/usr/bin/env python3
"""
Simple script to change admin password - run this on PythonAnywhere console.
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User
from werkzeug.security import generate_password_hash

def change_password_simple():
    """Simple password change for PythonAnywhere."""
    with app.app_context():
        try:
            print("🔐 Changing admin password to QingHe@81341...")
            
            # Find admin user
            admin_user = User.query.filter_by(is_admin=True).first()
            
            if not admin_user:
                print("❌ No admin user found!")
                return False
            
            # Update password
            new_password = "QingHe@81341"
            admin_user.password_hash = generate_password_hash(new_password)
            admin_user.has_default_password = False
            
            db.session.commit()
            
            print("✅ Admin password updated successfully!")
            print(f"   - Username: {admin_user.username}")
            print(f"   - Email: {admin_user.email}")
            print(f"   - New Password: {new_password}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            db.session.rollback()

if __name__ == '__main__':
    change_password_simple()
