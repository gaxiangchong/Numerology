#!/usr/bin/env python3
"""
Fix existing users who have email_verified = False
This script updates all existing users to have email_verified = True
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User

def fix_existing_users_email_verification():
    """Update all existing users to have email_verified = True."""
    print("🔧 Fixing Existing Users Email Verification")
    print("=" * 50)
    
    with app.app_context():
        try:
            # Find all users with email_verified = False
            unverified_users = User.query.filter_by(email_verified=False).all()
            
            if not unverified_users:
                print("✅ All users already have email_verified = True")
                return True
            
            print(f"📋 Found {len(unverified_users)} users with email_verified = False")
            print("Updating users:")
            
            for user in unverified_users:
                print(f"  • {user.username} ({user.email})")
                user.email_verified = True
            
            # Commit the changes
            db.session.commit()
            
            print(f"\n✅ Successfully updated {len(unverified_users)} users")
            print("All users now have email_verified = True")
            
            return True
            
        except Exception as e:
            print(f"❌ Error updating users: {e}")
            db.session.rollback()
            return False

def main():
    print("🔧 Fix Existing Users Email Verification")
    print("=" * 60)
    
    print("This script will update all existing users to have email_verified = True")
    print("This allows them to login without email verification.")
    
    proceed = input("\nProceed with the update? (y/N): ").strip().lower()
    
    if proceed == 'y':
        success = fix_existing_users_email_verification()
        
        if success:
            print("\n🎉 All users can now login without email verification!")
            print("🔄 Restart your Flask app to apply the changes")
        else:
            print("\n❌ Failed to update users")
    else:
        print("\n⏸️ Update cancelled")

if __name__ == '__main__':
    main()
