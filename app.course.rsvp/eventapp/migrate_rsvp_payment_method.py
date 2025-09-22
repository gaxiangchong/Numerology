#!/usr/bin/env python3
"""
Migration script to add payment_method field to RSVP model.
This script adds the payment_method column to the rsvp table.
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db

def migrate_rsvp_payment_method():
    """Add payment_method column to rsvp table."""
    print("🔄 Starting RSVP payment method migration...")
    
    try:
        with app.app_context():
            # Check if payment_method column already exists
            with db.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT COUNT(*) as count 
                    FROM pragma_table_info('rsvp') 
                    WHERE name = 'payment_method'
                """))
                column_exists = result.fetchone()[0] > 0
                
                if column_exists:
                    print("✅ payment_method column already exists. Migration not needed.")
                    return
                
                print("📝 Adding payment_method column to rsvp table...")
                
                # Add payment_method column
                conn.execute(text("""
                    ALTER TABLE rsvp 
                    ADD COLUMN payment_method VARCHAR(20)
                """))
                
                conn.commit()
                print("✅ Successfully added payment_method column!")
                
                # Set default payment_method for existing RSVPs based on payment_status
                print("💰 Setting default payment methods for existing RSVPs...")
                conn.execute(text("""
                    UPDATE rsvp 
                    SET payment_method = 'card' 
                    WHERE payment_status = 'paid' AND payment_method IS NULL
                """))
                
                conn.execute(text("""
                    UPDATE rsvp 
                    SET payment_method = 'free' 
                    WHERE payment_status = 'paid' AND payment_amount = 0.0 AND payment_method IS NULL
                """))
                
                conn.commit()
                print("✅ Successfully set default payment methods for existing RSVPs!")
                
                # Verify the migration
                result = conn.execute(text("""
                    SELECT COUNT(*) as count 
                    FROM rsvp 
                    WHERE payment_method IS NOT NULL
                """))
                rsvp_count = result.fetchone()[0]
                print(f"✅ Migration completed! {rsvp_count} RSVPs now have payment_method field.")
                
    except SQLAlchemyError as e:
        print(f"❌ Database error during migration: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during migration: {e}")
        return False
    
    return True

def rollback_rsvp_payment_method():
    """Remove payment_method column from rsvp table."""
    print("🔄 Rolling back RSVP payment method migration...")
    
    try:
        with app.app_context():
            with db.engine.connect() as conn:
                # Check if payment_method column exists
                result = conn.execute(text("""
                    SELECT COUNT(*) as count 
                    FROM pragma_table_info('rsvp') 
                    WHERE name = 'payment_method'
                """))
                column_exists = result.fetchone()[0] > 0
                
                if not column_exists:
                    print("ℹ️ payment_method column does not exist. Nothing to rollback.")
                    return
                
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
    print("💳 RSVP Payment Method Migration Tool")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == "rollback":
        success = rollback_rsvp_payment_method()
    else:
        success = migrate_rsvp_payment_method()
    
    if success:
        print("\n🎉 Migration completed successfully!")
        print("\n📋 Next steps:")
        print("1. Restart your Flask application")
        print("2. Test the integrated RSVP/payment system")
        print("3. Verify credit payments work correctly")
    else:
        print("\n❌ Migration failed!")
        print("Please check the error messages above and try again.")
    
    print("=" * 50)
