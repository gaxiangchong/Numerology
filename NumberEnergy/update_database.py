#!/usr/bin/env python3
"""
Script to update the database with the new UserHistory table
"""

import os
import sys

# Add the mysite directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mysite'))

# Change to the mysite directory
os.chdir(os.path.join(os.path.dirname(__file__), 'mysite'))

# Import and run the app
from app import app, db

def update_database():
    """Create the new UserHistory table"""
    with app.app_context():
        try:
            # Create all tables (this will add the new UserHistory table)
            db.create_all()
            print("✅ Database updated successfully!")
            print("✅ UserHistory table created")
            print("✅ Recent numbers feature is now ready!")
        except Exception as e:
            print(f"❌ Error updating database: {e}")

if __name__ == '__main__':
    update_database()
