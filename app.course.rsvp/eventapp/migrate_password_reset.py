#!/usr/bin/env python3
"""
Database migration script to add password reset fields to existing User table.

This script adds the following fields to the User model:
- password_reset_token: String field to store password reset tokens
- password_reset_sent_at: DateTime field to track when password reset was sent

Run this script after updating the User model in app.py.
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User

def migrate_password_reset():
    """Add password reset fields to existing User table."""
    print("Starting password reset migration...")
    
    with app.app_context():
        try:
            # Check if the new columns already exist
            inspector = db.inspect(db.engine)
            existing_columns = [col['name'] for col in inspector.get_columns('user')]
            
            if 'password_reset_token' in existing_columns and 'password_reset_sent_at' in existing_columns:
                print("✅ Password reset fields already exist in the database.")
                return
            
            print("Adding password reset fields to User table...")
            
            # Add the new columns
            with db.engine.connect() as conn:
                conn.execute(db.text('ALTER TABLE user ADD COLUMN password_reset_token VARCHAR(100)'))
                conn.execute(db.text('ALTER TABLE user ADD COLUMN password_reset_sent_at DATETIME'))
                conn.commit()
            
            print("✅ Successfully added password reset fields to User table.")
            print("🎉 Password reset migration completed successfully!")
            
        except Exception as e:
            print(f"❌ Error during migration: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    migrate_password_reset()
