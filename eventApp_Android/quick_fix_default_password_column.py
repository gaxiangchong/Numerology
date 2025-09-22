#!/usr/bin/env python3
"""
Quick fix script to add has_default_password column to User table.
This script can be run directly in PythonAnywhere console.
"""

import sqlite3
import os

def add_default_password_column():
    """Add has_default_password column to User table."""
    print("🔄 Adding has_default_password column to User table...")
    
    # Database path
    db_path = 'instance/eventapp.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        return False
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
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

if __name__ == "__main__":
    add_default_password_column()
