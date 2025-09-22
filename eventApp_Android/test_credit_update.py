#!/usr/bin/env python3
"""
Test script to verify credit point updates are working correctly.
"""

import os
import sys
from sqlalchemy import create_engine, text

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User

def test_credit_update():
    """Test credit point updates."""
    print("🧪 Testing Credit Point Updates...")
    
    try:
        with app.app_context():
            # Get a test user
            user = User.query.first()
            if not user:
                print("❌ No users found in database")
                return False
            
            print(f"📝 Testing with user: {user.username}")
            print(f"💰 Original credits: {user.credit_point}")
            
            # Test credit update
            original_credits = user.credit_point
            test_credits = 150.75
            
            user.credit_point = test_credits
            db.session.commit()
            
            # Verify update
            updated_user = User.query.get(user.id)
            print(f"✅ Updated credits: {updated_user.credit_point}")
            
            if updated_user.credit_point == test_credits:
                print("✅ Credit update successful!")
            else:
                print("❌ Credit update failed!")
                return False
            
            # Restore original credits
            user.credit_point = original_credits
            db.session.commit()
            print(f"🔄 Restored original credits: {original_credits}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

def show_all_credits():
    """Show all users' current credit points."""
    print("\n📊 Current Credit Points:")
    print("=" * 40)
    
    try:
        with app.app_context():
            users = User.query.all()
            for user in users:
                print(f"👤 {user.username:<15} | 💰 {user.credit_point:>8.2f}")
            
    except Exception as e:
        print(f"❌ Error showing credits: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("🏦 Credit Update Test")
    print("=" * 50)
    
    show_all_credits()
    success = test_credit_update()
    
    if success:
        print("\n✅ Credit system is working correctly!")
        print("\n📋 To test in the web interface:")
        print("1. Go to Admin → Member Management")
        print("2. Click edit on any member")
        print("3. Change the credit points")
        print("4. Save with superuser password")
        print("5. Check if the table updates")
    else:
        print("\n❌ Credit system has issues!")
    
    print("=" * 50)
