#!/usr/bin/env python3
"""
Migration script to add credit_point field to User model.
This script adds the credit_point column to the users table.
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db

def migrate_credit_system():
    """Add credit_point column to users table."""
    print("🔄 Starting credit system migration...")
    
    try:
        with app.app_context():
            # Check if credit_point column already exists
            with db.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT COUNT(*) as count 
                    FROM pragma_table_info('user') 
                    WHERE name = 'credit_point'
                """))
                column_exists = result.fetchone()[0] > 0
                
                if column_exists:
                    print("✅ credit_point column already exists. Migration not needed.")
                    return
                
                print("📝 Adding credit_point column to users table...")
                
                # Add credit_point column
                conn.execute(text("""
                    ALTER TABLE user 
                    ADD COLUMN credit_point REAL DEFAULT 0.0
                """))
                
                conn.commit()
                print("✅ Successfully added credit_point column!")
                
                # Set default credit points for existing users
                print("💰 Setting default credit points for existing users...")
                conn.execute(text("""
                    UPDATE user 
                    SET credit_point = 0.0 
                    WHERE credit_point IS NULL
                """))
                
                conn.commit()
                print("✅ Successfully set default credit points for existing users!")
                
                # Verify the migration
                result = conn.execute(text("""
                    SELECT COUNT(*) as count 
                    FROM user 
                    WHERE credit_point IS NOT NULL
                """))
                user_count = result.fetchone()[0]
                print(f"✅ Migration completed! {user_count} users now have credit_point field.")
                
    except SQLAlchemyError as e:
        print(f"❌ Database error during migration: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during migration: {e}")
        return False
    
    return True

def rollback_credit_system():
    """Remove credit_point column from users table."""
    print("🔄 Rolling back credit system migration...")
    
    try:
        with app.app_context():
            with db.engine.connect() as conn:
                # Check if credit_point column exists
                result = conn.execute(text("""
                    SELECT COUNT(*) as count 
                    FROM pragma_table_info('user') 
                    WHERE name = 'credit_point'
                """))
                column_exists = result.fetchone()[0] > 0
                
                if not column_exists:
                    print("ℹ️ credit_point column does not exist. Nothing to rollback.")
                    return
                
                print("📝 Removing credit_point column from users table...")
                
                # Note: SQLite doesn't support DROP COLUMN directly
                # We need to recreate the table without the credit_point column
                print("⚠️ SQLite doesn't support DROP COLUMN. Manual table recreation required.")
                print("⚠️ This rollback is not implemented for safety reasons.")
                print("⚠️ If you need to remove the column, please backup your data first.")
                
    except SQLAlchemyError as e:
        print(f"❌ Database error during rollback: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during rollback: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("🏦 Credit System Migration Tool")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == "rollback":
        success = rollback_credit_system()
    else:
        success = migrate_credit_system()
    
    if success:
        print("\n🎉 Migration completed successfully!")
        print("\n📋 Next steps:")
        print("1. Restart your Flask application")
        print("2. Test the credit system in member management")
        print("3. Verify credit points are displayed correctly")
    else:
        print("\n❌ Migration failed!")
        print("Please check the error messages above and try again.")
    
    print("=" * 50)
