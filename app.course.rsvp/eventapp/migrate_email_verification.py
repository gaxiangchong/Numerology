#!/usr/bin/env python3
"""
Database migration script to add email verification fields to existing User table.

This script adds the following fields to the User model:
- email_verification_token: String field to store verification tokens
- email_verification_sent_at: DateTime field to track when verification was sent

Run this script after updating the User model in app.py.
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User

def migrate_email_verification():
    """Add email verification fields to existing User table."""
    print("Starting email verification migration...")
    
    with app.app_context():
        try:
            # Check if the new columns already exist
            inspector = db.inspect(db.engine)
            existing_columns = [col['name'] for col in inspector.get_columns('user')]
            
            if 'email_verification_token' in existing_columns and 'email_verification_sent_at' in existing_columns:
                print("✅ Email verification fields already exist in the database.")
                return
            
            print("Adding email verification fields to User table...")
            
            # Add the new columns
            with db.engine.connect() as conn:
                conn.execute(db.text('ALTER TABLE user ADD COLUMN email_verification_token VARCHAR(100)'))
                conn.execute(db.text('ALTER TABLE user ADD COLUMN email_verification_sent_at DATETIME'))
                conn.commit()
            
            print("✅ Successfully added email verification fields to User table.")
            
            # Update existing users to have email_verified = True (grandfather existing users)
            existing_users = User.query.filter_by(email_verified=False).all()
            if existing_users:
                print(f"Updating {len(existing_users)} existing users to have verified emails...")
                for user in existing_users:
                    user.email_verified = True
                db.session.commit()
                print("✅ Updated existing users to have verified emails.")
            
            print("🎉 Email verification migration completed successfully!")
            
        except Exception as e:
            print(f"❌ Error during migration: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    migrate_email_verification()
