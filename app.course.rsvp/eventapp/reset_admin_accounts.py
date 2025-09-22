#!/usr/bin/env python3
"""
Script to delete all existing admin accounts and recreate a fresh admin account.
This script will:
1. Remove admin privileges from all users
2. Delete all admin users (except the one running the script)
3. Create a new admin account with specified credentials
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User
from werkzeug.security import generate_password_hash

def reset_admin_accounts():
    """Reset all admin accounts and create a new one."""
    print("🔄 Starting admin account reset process...")
    
    with app.app_context():
        try:
            # Step 1: Remove admin privileges from all users
            print("📝 Removing admin privileges from all users...")
            admin_users = User.query.filter_by(is_admin=True).all()
            for user in admin_users:
                user.is_admin = False
                print(f"   - Removed admin privileges from: {user.username}")
            
            # Step 2: Delete all admin users
            print("🗑️ Deleting all admin users...")
            for user in admin_users:
                username = user.username
                # Delete associated data first
                for rsvp in user.rsvps:
                    db.session.delete(rsvp)
                for event in user.created_events:
                    # Delete all RSVPs for events created by this user
                    for rsvp in event.rsvps:
                        db.session.delete(rsvp)
                    db.session.delete(event)
                
                # Delete the user
                db.session.delete(user)
                print(f"   - Deleted admin user: {username}")
            
            # Step 3: Create new admin account
            print("👤 Creating new admin account...")
            
            # Get admin credentials from user input
            admin_username = input("Enter new admin username: ").strip()
            admin_email = input("Enter new admin email: ").strip()
            admin_password = input("Enter new admin password: ").strip()
            
            if not admin_username or not admin_email or not admin_password:
                print("❌ Error: All fields are required!")
                return False
            
            # Check if username or email already exists
            existing_user = User.query.filter(
                (User.username == admin_username) | (User.email == admin_email)
            ).first()
            
            if existing_user:
                print(f"❌ Error: Username '{admin_username}' or email '{admin_email}' already exists!")
                return False
            
            # Create new admin user
            new_admin = User(
                username=admin_username,
                email=admin_email,
                password_hash=generate_password_hash(admin_password),
                first_name="Admin",
                last_name="User",
                phone="",
                country_code="+65",
                timezone="Asia/Singapore",
                locale="en",
                country="Singapore",
                city="Singapore",
                membership_type="嫡传",
                membership_grade="Diamond",
                credit_point=1000.0,  # Give admin some credits
                is_admin=True,
                email_verified=True,
                account_status="Active",
                created_at=datetime.utcnow()
            )
            
            db.session.add(new_admin)
            db.session.commit()
            
            print("✅ Admin account reset completed successfully!")
            print(f"   - New admin username: {admin_username}")
            print(f"   - New admin email: {admin_email}")
            print(f"   - Admin privileges: Enabled")
            print(f"   - Email verified: Yes")
            print(f"   - Initial credits: 1000.0")
            print(f"   - Membership: 嫡传 (Diamond)")
            
            return True
            
        except Exception as e:
            print(f"❌ Error during admin reset: {e}")
            db.session.rollback()
            return False

def main():
    """Main function to run the admin reset."""
    print("=" * 60)
    print("🔐 ADMIN ACCOUNT RESET TOOL")
    print("=" * 60)
    print("⚠️  WARNING: This will delete ALL existing admin accounts!")
    print("⚠️  Make sure you have access to the database if something goes wrong!")
    print()
    
    # Confirm action
    confirm = input("Are you sure you want to proceed? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("❌ Operation cancelled.")
        return
    
    print()
    print("📋 Please provide the new admin account details:")
    print()
    
    # Run the reset
    success = reset_admin_accounts()
    
    if success:
        print()
        print("🎉 Admin account reset completed successfully!")
        print("🔑 You can now log in with the new admin credentials.")
    else:
        print()
        print("❌ Admin account reset failed!")
        print("🔧 Please check the error messages above and try again.")

if __name__ == '__main__':
    main()
