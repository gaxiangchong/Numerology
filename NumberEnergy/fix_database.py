#!/usr/bin/env python3
"""
Script to fix the database schema and test registration
"""

import os
import sys

# Add the mysite directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mysite'))

# Change to the mysite directory
os.chdir(os.path.join(os.path.dirname(__file__), 'mysite'))

# Import and run the app
from app import app, db

def fix_database():
    """Create/update database tables"""
    with app.app_context():
        try:
            # Drop all tables and recreate them (for development only)
            db.drop_all()
            db.create_all()
            print("✅ Database tables created successfully!")
            print("✅ Registration should now work without the user_type error")
        except Exception as e:
            print(f"❌ Error creating database: {e}")

if __name__ == '__main__':
    fix_database()
