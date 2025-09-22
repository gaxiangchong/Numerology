#!/usr/bin/env python3
"""
Admin user setup script for EventApp.

This script creates an admin user for the application.
Run this script after setting up the database.
"""

import os
import sys
from getpass import getpass

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User

def create_admin_user():
    """Create an admin user interactively."""
    print("EventApp Admin User Setup")
    print("=" * 30)
    
    # Check if admin already exists
    with app.app_context():
        existing_admin = User.query.filter_by(is_admin=True).first()
        if existing_admin:
            print(f"Admin user already exists: {existing_admin.username} ({existing_admin.email})")
            response = input("Do you want to create another admin user? (y/N): ")
            if response.lower() != 'y':
                print("Exiting...")
                return
    
    # Get admin details
    username = input("Enter admin username: ").strip()
    if not username:
        print("Username cannot be empty!")
        return
    
    email = input("Enter admin email: ").strip().lower()
    if not email:
        print("Email cannot be empty!")
        return
    
    # Validate email format
    import re
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        print("Invalid email format!")
        return
    
    # Check if email already exists
    with app.app_context():
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f"User with email {email} already exists!")
            return
    
    password = getpass("Enter admin password: ")
    if len(password) < 6:
        print("Password must be at least 6 characters long!")
        return
    
    confirm_password = getpass("Confirm admin password: ")
    if password != confirm_password:
        print("Passwords do not match!")
        return
    
    # Create admin user
    try:
        with app.app_context():
            admin = User(
                username=username,
                email=email,
                is_admin=True,
                email_notifications=True,
                email_verified=True  # Skip email verification for admin accounts
            )
            admin.set_password(password)
            db.session.add(admin)
            db.session.commit()
            
            print(f"\n✅ Admin user created successfully!")
            print(f"Username: {username}")
            print(f"Email: {email}")
            print(f"Admin privileges: Yes")
            print("\nYou can now log in and create events.")
            
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        return

def list_users():
    """List all users in the system."""
    with app.app_context():
        users = User.query.all()
        if not users:
            print("No users found in the system.")
            return
        
        print("\nCurrent Users:")
        print("-" * 50)
        for user in users:
            admin_status = "Admin" if user.is_admin else "User"
            verified_status = "Verified" if user.email_verified else "Unverified"
            print(f"{user.username} ({user.email}) - {admin_status} - {verified_status}")

def fix_admin_verification():
    """Fix email verification for existing admin accounts."""
    print("🔧 Fixing Email Verification for Admin Accounts")
    print("=" * 50)
    
    with app.app_context():
        admin_users = User.query.filter_by(is_admin=True).all()
        
        if not admin_users:
            print("No admin users found.")
            return
        
        print(f"Found {len(admin_users)} admin user(s):")
        for admin in admin_users:
            print(f"  - {admin.username} ({admin.email})")
            if not admin.email_verified:
                print(f"    ❌ Email not verified - fixing...")
                admin.email_verified = True
                db.session.commit()
                print(f"    ✅ Email verification enabled")
            else:
                print(f"    ✅ Email already verified")
        
        print("\n✅ All admin accounts now have email verification enabled!")

def main():
    """Main function."""
    print("EventApp Setup Utility")
    print("=" * 20)
    print("1. Create admin user")
    print("2. List all users")
    print("3. Fix admin email verification")
    print("4. Exit")
    
    while True:
        choice = input("\nSelect an option (1-4): ").strip()
        
        if choice == '1':
            create_admin_user()
            break
        elif choice == '2':
            list_users()
        elif choice == '3':
            fix_admin_verification()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")

if __name__ == '__main__':
    main()
