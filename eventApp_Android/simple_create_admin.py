#!/usr/bin/env python3
"""
Simple script to create an admin user directly in the database.
This script works without Flask imports.
"""

import sqlite3
import os
import hashlib
import re

def create_admin_user():
    """Create an admin user directly in the database."""
    print("🔧 EventApp Admin User Setup (Direct Database)")
    print("=" * 50)
    
    # Database path
    db_path = 'instance/eventapp.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        print("   Make sure you're in the eventapp directory")
        return False
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"📁 Database found: {db_path}")
        
        # Check if admin already exists
        cursor.execute("SELECT username, email FROM user WHERE is_admin = 1")
        existing_admins = cursor.fetchall()
        
        if existing_admins:
            print("✅ Existing admin users:")
            for admin in existing_admins:
                print(f"   - {admin[0]} ({admin[1]})")
            
            response = input("\nDo you want to create another admin user? (y/N): ")
            if response.lower() != 'y':
                print("Exiting...")
                conn.close()
                return True
        
        # Get admin details
        print("\n📝 Enter admin user details:")
        username = input("Username: ").strip()
        if not username:
            print("❌ Username cannot be empty!")
            conn.close()
            return False
        
        email = input("Email: ").strip().lower()
        if not email:
            print("❌ Email cannot be empty!")
            conn.close()
            return False
        
        # Validate email format
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            print("❌ Invalid email format!")
            conn.close()
            return False
        
        # Check if email already exists
        cursor.execute("SELECT id FROM user WHERE email = ?", (email,))
        if cursor.fetchone():
            print(f"❌ User with email {email} already exists!")
            conn.close()
            return False
        
        # Get password
        password = input("Password: ")
        if not password:
            print("❌ Password cannot be empty!")
            conn.close()
            return False
        
        if len(password) < 6:
            print("❌ Password must be at least 6 characters long!")
            conn.close()
            return False
        
        confirm_password = input("Confirm password: ")
        if password != confirm_password:
            print("❌ Passwords do not match!")
            conn.close()
            return False
        
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
        
        # Hash password (using werkzeug's method)
        from werkzeug.security import generate_password_hash
        password_hash = generate_password_hash(password)
        
        # Create admin user
        cursor.execute("""
            INSERT INTO user (
                username, email, password_hash, phone, membership_type, 
                membership_grade, is_admin, email_verified, account_status, 
                has_default_password, country, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """, (
            username, email, password_hash, phone or None, membership_type,
            'Pending Review', 1, 1, 'active', 0, 'Singapore'
        ))
        
        # Commit changes
        conn.commit()
        
        # Get the new user ID
        user_id = cursor.lastrowid
        
        print("\n" + "=" * 50)
        print("🎉 ADMIN USER CREATED SUCCESSFULLY!")
        print("=" * 50)
        print(f"✅ User ID: {user_id}")
        print(f"✅ Username: {username}")
        print(f"✅ Email: {email}")
        print(f"✅ Membership Type: {membership_type}")
        print(f"✅ Admin Privileges: Yes")
        print(f"✅ Email Verified: Yes")
        print(f"✅ Phone: {phone or 'Not provided'}")
        print("\n🚀 You can now login with these credentials!")
        
        conn.close()
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Trying alternative password hashing...")
        
        # Fallback: simple password hash
        try:
            import hashlib
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            # Create admin user with simple hash
            cursor.execute("""
                INSERT INTO user (
                    username, email, password_hash, phone, membership_type, 
                    membership_grade, is_admin, email_verified, account_status, 
                    has_default_password, country, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
            """, (
                username, email, password_hash, phone or None, membership_type,
                'Pending Review', 1, 1, 'active', 0, 'Singapore'
            ))
            
            conn.commit()
            user_id = cursor.lastrowid
            
            print("\n" + "=" * 50)
            print("🎉 ADMIN USER CREATED SUCCESSFULLY!")
            print("=" * 50)
            print(f"✅ User ID: {user_id}")
            print(f"✅ Username: {username}")
            print(f"✅ Email: {email}")
            print(f"✅ Membership Type: {membership_type}")
            print(f"✅ Admin Privileges: Yes")
            print(f"✅ Email Verified: Yes")
            print(f"✅ Phone: {phone or 'Not provided'}")
            print("\n🚀 You can now login with these credentials!")
            
            conn.close()
            return True
            
        except Exception as e2:
            print(f"❌ Fallback error: {e2}")
            if 'conn' in locals():
                conn.close()
            return False
            
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        if 'conn' in locals():
            conn.close()
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        if 'conn' in locals():
            conn.close()
        return False

if __name__ == "__main__":
    create_admin_user()
