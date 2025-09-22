#!/usr/bin/env python3
"""
Migration script to add has_default_password field to existing User table.
This script adds the new column and sets default values for existing users.
"""

import os
import sys
import sqlite3

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def migrate_add_default_password_field():
    """Add has_default_password field to User table."""
    print("🔄 Adding has_default_password field to User table...")
    print("=" * 60)
    
    try:
        # Check if we're in the right directory
        if not os.path.exists('instance/eventapp.db'):
            print("❌ Database not found. Make sure you're in the eventapp directory.")
            return False
        
        # Connect to database
        conn = sqlite3.connect('instance/eventapp.db')
        cursor = conn.cursor()
        
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
        
        # Update existing users to have has_default_password = False
        cursor.execute("UPDATE user SET has_default_password = 0 WHERE has_default_password IS NULL")
        
        # Commit changes
        conn.commit()
        
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

def test_migration():
    """Test the migration by checking the database structure."""
    print("\n🧪 Testing migration...")
    
    try:
        conn = sqlite3.connect('instance/eventapp.db')
        cursor = conn.cursor()
        
        # Check table structure
        cursor.execute("PRAGMA table_info(user)")
        columns = cursor.fetchall()
        
        print("📋 Current User table structure:")
        for column in columns:
            print(f"   - {column[1]} ({column[2]}) - Default: {column[4]}")
        
        # Check if has_default_password column exists
        has_default_password_exists = any(col[1] == 'has_default_password' for col in columns)
        
        if has_default_password_exists:
            print("✅ has_default_password column is present")
            
            # Check user data
            cursor.execute("SELECT COUNT(*) FROM user WHERE has_default_password = 1")
            default_password_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM user WHERE has_default_password = 0")
            normal_password_count = cursor.fetchone()[0]
            
            print(f"📊 Users with default password: {default_password_count}")
            print(f"📊 Users with normal password: {normal_password_count}")
        else:
            print("❌ has_default_password column is missing")
        
        conn.close()
        return has_default_password_exists
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        if 'conn' in locals():
            conn.close()
        return False

def main():
    """Main function to run the migration."""
    print("🚀 Password Reset Feature Migration")
    print("=" * 60)
    
    # Run migration
    success = migrate_add_default_password_field()
    
    if success:
        # Test the migration
        test_success = test_migration()
        
        if test_success:
            print("\n" + "=" * 60)
            print("✅ MIGRATION COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print("📋 What was added:")
            print("   - has_default_password column to User table")
            print("   - Default value of False for existing users")
            print("\n🚀 Password reset feature is now ready!")
            print("\n📖 Next steps:")
            print("   1. Deploy the updated code")
            print("   2. Test password reset functionality")
            print("   3. Train admins on the new feature")
        else:
            print("\n❌ Migration completed but test failed. Please check the database.")
    else:
        print("\n❌ Migration failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
