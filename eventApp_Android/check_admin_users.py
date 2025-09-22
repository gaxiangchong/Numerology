#!/usr/bin/env python3
"""
Check existing admin users in the database.
"""

import sqlite3

def check_admin_users():
    """Check existing admin users."""
    print("🔍 Checking Admin Users...")
    print("=" * 30)
    
    try:
        conn = sqlite3.connect('instance/eventapp.db')
        cursor = conn.cursor()
        
        # Get all admin users
        cursor.execute("SELECT id, username, email, is_admin, email_verified FROM user WHERE is_admin = 1")
        admins = cursor.fetchall()
        
        if admins:
            print(f"✅ Found {len(admins)} admin user(s):")
            for admin in admins:
                print(f"   ID: {admin[0]}")
                print(f"   Username: {admin[1]}")
                print(f"   Email: {admin[2]}")
                print(f"   Admin: {admin[3]}")
                print(f"   Email Verified: {admin[4]}")
                print()
        else:
            print("❌ No admin users found!")
        
        # Get all users
        cursor.execute("SELECT COUNT(*) FROM user")
        total_users = cursor.fetchone()[0]
        print(f"📊 Total users in database: {total_users}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_admin_users()
