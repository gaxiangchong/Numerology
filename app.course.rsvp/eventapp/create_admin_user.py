#!/usr/bin/env python3
"""
Simple script to create an admin user for EventApp.
This script creates an admin user interactively.
"""

import os
import sys
import re
from getpass import getpass

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_admin_user():
    """Create an admin user interactively."""
    print("🔧 EventApp Admin User Setup")
    print("=" * 40)
    
    try:
        from app import app, db, User
        
        with app.app_context():
            # Check if admin already exists
            existing_admin = User.query.filter_by(is_admin=True).first()
            if existing_admin:
                print(f"✅ Admin user already exists: {existing_admin.username} ({existing_admin.email})")
                response = input("Do you want to create another admin user? (y/N): ")
                if response.lower() != 'y':
                    print("Exiting...")
                    return
            
            # Get admin details
            print("\n📝 Enter admin user details:")
            username = input("Username: ").strip()
            if not username:
                print("❌ Username cannot be empty!")
                return
            
            email = input("Email: ").strip().lower()
            if not email:
                print("❌ Email cannot be empty!")
                return
            
            # Validate email format
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                print("❌ Invalid email format!")
                return
            
            # Check if email already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                print(f"❌ User with email {email} already exists!")
                return
            
            # Get password
            password = getpass("Password: ")
            if not password:
                print("❌ Password cannot be empty!")
                return
            
            if len(password) < 6:
                print("❌ Password must be at least 6 characters long!")
                return
            
            confirm_password = getpass("Confirm password: ")
            if password != confirm_password:
                print("❌ Passwords do not match!")
                return
            
            # Get phone number
            phone = input("Phone number (optional): ").strip()
            
            # Get membership type
            print("\n📋 Membership Type Options:")
            print("1. NA")
            print("2. 会员")
            print("3. 家族")
            print("4. 星光")
            print("5. 嫡传")
            
            membership_choice = input("Select membership type (1-5, default: 1): ").strip()
            membership_types = {
                '1': 'NA',
                '2': '会员',
                '3': '家族',
                '4': '星光',
                '5': '嫡传'
            }
            membership_type = membership_types.get(membership_choice, 'NA')
            
            # Create admin user
            admin_user = User(
                username=username,
                email=email,
                phone=phone or None,
                membership_type=membership_type,
                membership_grade='Pending Review',
                is_admin=True,
                email_verified=True,  # Admin users are auto-verified
                account_status='active',
                has_default_password=False,  # Admin sets their own password
                country='Singapore'
            )
            admin_user.set_password(password)
            
            # Add to database
            db.session.add(admin_user)
            db.session.commit()
            
            print("\n" + "=" * 40)
            print("🎉 ADMIN USER CREATED SUCCESSFULLY!")
            print("=" * 40)
            print(f"✅ Username: {username}")
            print(f"✅ Email: {email}")
            print(f"✅ Membership Type: {membership_type}")
            print(f"✅ Admin Privileges: Yes")
            print(f"✅ Email Verified: Yes")
            print("\n🚀 You can now login with these credentials!")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure you're in the eventapp directory and Flask is installed")
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")

if __name__ == "__main__":
    create_admin_user()