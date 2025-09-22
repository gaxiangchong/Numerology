#!/usr/bin/env python3
"""
Fix local database by adding has_default_password column.
Run this script to update your local database.
"""

import sqlite3
import os

def fix_local_database():
    """Add has_default_password column to local database."""
    print("🔧 Fixing Local Database...")
    print("=" * 40)
    
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
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'has_default_password' in columns:
            print("✅ has_default_password column already exists.")
            conn.close()
            return True
        
        print("📝 Adding has_default_password column...")
        
        # Add the new column
        cursor.execute("ALTER TABLE user ADD COLUMN has_default_password BOOLEAN DEFAULT 0")
        print("   ✅ Column added")
        
        # Update existing users to have has_default_password = False
        cursor.execute("UPDATE user SET has_default_password = 0 WHERE has_default_password IS NULL")
        print("   ✅ Existing users updated")
        
        # Commit changes
        conn.commit()
        print("   ✅ Changes committed")
        
        # Verify the column was added
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'has_default_password' in columns:
            print("✅ has_default_password column added successfully!")
            
            # Show user count
            cursor.execute("SELECT COUNT(*) FROM user")
            user_count = cursor.fetchone()[0]
            print(f"📊 Updated {user_count} existing users with has_default_password = False")
            
            conn.close()
            return True
        else:
            print("❌ Failed to add has_default_password column.")
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
    success = fix_local_database()
    
    if success:
        print("\n" + "=" * 40)
        print("🎉 DATABASE FIXED SUCCESSFULLY!")
        print("=" * 40)
        print("✅ You can now:")
        print("   1. Start your Flask app")
        print("   2. Test the password reset feature")
        print("   3. Login and test member management")
        print("\n🚀 Ready to test!")
    else:
        print("\n❌ Database fix failed. Please check the error messages above.")
