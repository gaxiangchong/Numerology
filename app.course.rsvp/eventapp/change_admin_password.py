#!/usr/bin/env python3
"""
Script to change admin password to QingHe@81341
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User
from werkzeug.security import generate_password_hash

def change_admin_password():
    """Change admin password to QingHe@81341"""
    with app.app_context():
        try:
            print("🔐 Changing admin password...")
            
            # Find admin user
            admin_user = User.query.filter_by(is_admin=True).first()
            
            if not admin_user:
                print("❌ No admin user found!")
                return False
            
            # Update password
            new_password = "QingHe@81341"
            admin_user.password_hash = generate_password_hash(new_password)
            admin_user.has_default_password = False  # Mark as not default password
            
            db.session.commit()
            
            print("✅ Admin password updated successfully!")
            print(f"   - Username: {admin_user.username}")
            print(f"   - Email: {admin_user.email}")
            print(f"   - New Password: {new_password}")
            print("   - Password is now secure (not default)")
            
            return True
            
        except Exception as e:
            print(f"❌ Error changing password: {e}")
            db.session.rollback()
            return False

def main():
    """Main function to change admin password."""
    print("=" * 50)
    print("🔐 ADMIN PASSWORD CHANGE TOOL")
    print("=" * 50)
    print("This will change the admin password to: QingHe@81341")
    print()
    
    # Run the password change
    success = change_admin_password()
    
    if success:
        print()
        print("🎉 Admin password changed successfully!")
        print("🔑 You can now log in with the new password.")
    else:
        print()
        print("❌ Password change failed!")
        print("🔧 Please check the error messages above and try again.")

if __name__ == '__main__':
    main()
