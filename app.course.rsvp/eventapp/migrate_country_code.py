#!/usr/bin/env python3
"""
Database migration script to add country_code column to User table.

This script adds the country_code field to the User model:
- country_code: String field to store country codes like +65, +1, etc.

Run this script to fix the OperationalError: no such column: user.country_code
"""

import os
import sys
import sqlite3
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db

def migrate_country_code():
    """Add country_code column to User table."""
    print("🔄 Starting country_code migration...")
    
    try:
        with app.app_context():
            # Get the database file path
            db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
            if not db_path.startswith('/') and not db_path.startswith('C:'):
                # If it's a relative path, look in the instance directory
                db_path = os.path.join('instance', db_path)
            
            if not os.path.exists(db_path):
                print("❌ Database file not found. Creating new database...")
                db.create_all()
                print("✅ New database created with all tables and columns.")
                return
            
            # Check if country_code column already exists
            with db.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT COUNT(*) as count 
                    FROM pragma_table_info('user') 
                    WHERE name = 'country_code'
                """))
                column_exists = result.fetchone()[0] > 0
                
                if column_exists:
                    print("✅ country_code column already exists. Migration not needed.")
                    return
                
                print("📝 Adding country_code column to User table...")
                
                # Add country_code column
                conn.execute(text("""
                    ALTER TABLE user 
                    ADD COLUMN country_code VARCHAR(5)
                """))
                
                conn.commit()
                print("✅ Successfully added country_code column!")
                
                # Set default country code for existing users (Singapore +65)
                print("🌏 Setting default country code for existing users...")
                conn.execute(text("""
                    UPDATE user 
                    SET country_code = '+65' 
                    WHERE country_code IS NULL
                """))
                
                conn.commit()
                print("✅ Successfully set default country code for existing users!")
                
                # Verify the column was added
                result = conn.execute(text("""
                    SELECT name, type 
                    FROM pragma_table_info('user') 
                    WHERE name = 'country_code'
                """))
                column_info = result.fetchone()
                if column_info:
                    print(f"✅ Verified: country_code column added as {column_info[1]}")
                else:
                    print("❌ Warning: Could not verify country_code column was added")
                
                print("🎉 Country code migration completed successfully!")
                
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        raise

if __name__ == '__main__':
    migrate_country_code()
