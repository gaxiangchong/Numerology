#!/usr/bin/env python3
"""
Simple script to reset admin accounts - run this on PythonAnywhere console.
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User
from werkzeug.security import generate_password_hash

def reset_admin_simple():
    """Simple admin reset for PythonAnywhere."""
    with app.app_context():
        try:
            print("🔄 Resetting admin accounts...")
            
            # Remove admin privileges from all users
            admin_users = User.query.filter_by(is_admin=True).all()
            for user in admin_users:
                user.is_admin = False
                print(f"   - Removed admin from: {user.username}")
            
            # Delete all admin users
            for user in admin_users:
                username = user.username
                # Delete associated data
                for rsvp in user.rsvps:
                    db.session.delete(rsvp)
                for event in user.created_events:
                    for rsvp in event.rsvps:
                        db.session.delete(rsvp)
                    db.session.delete(event)
                db.session.delete(user)
                print(f"   - Deleted: {username}")
            
            # Create new admin
            new_admin = User(
                username='admin',
                email='admin@event.mynoblequest.com',
                password_hash=generate_password_hash('admin123'),
                first_name='Admin',
                last_name='User',
                phone='',
                country_code='+65',
                timezone='Asia/Singapore',
                locale='en',
                country='Singapore',
                city='Singapore',
                membership_type='嫡传',
                membership_grade='Diamond',
                credit_point=1000.0,
                is_admin=True,
                email_verified=True,
                account_status='Active',
                created_at=datetime.utcnow()
            )
            
            db.session.add(new_admin)
            db.session.commit()
            
            print("✅ New admin created:")
            print("   - Username: admin")
            print("   - Email: admin@event.mynoblequest.com")
            print("   - Password: admin123")
            print("   - Please change password after first login!")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            db.session.rollback()

if __name__ == '__main__':
    reset_admin_simple()
