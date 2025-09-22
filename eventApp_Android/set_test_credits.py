#!/usr/bin/env python3
"""
Script to set test credit points for users to verify table display.
"""

import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User

def set_test_credits():
    """Set test credit points for users."""
    print("💰 Setting test credit points...")
    
    try:
        with app.app_context():
            users = User.query.all()
            
            # Set different credit amounts for testing
            test_credits = [100.50, 250.00, 75.25, 500.00, 0.00]
            
            for i, user in enumerate(users):
                if i < len(test_credits):
                    user.credit_point = test_credits[i]
                    print(f"✅ Set {user.username} credits to {test_credits[i]}")
                else:
                    user.credit_point = 0.0
                    print(f"✅ Set {user.username} credits to 0.0")
            
            db.session.commit()
            print("\n🎉 Test credit points set successfully!")
            
            # Show summary
            print("\n📊 Updated Credit Points:")
            print("=" * 40)
            for user in users:
                print(f"👤 {user.username:<15} | 💰 {user.credit_point:>8.2f}")
            
    except Exception as e:
        print(f"❌ Error setting test credits: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("🏦 Set Test Credit Points")
    print("=" * 50)
    
    set_test_credits()
    
    print("\n📋 Now test in the web interface:")
    print("1. Go to Admin → Member Management")
    print("2. Check if credit points are displayed correctly")
    print("3. Try editing a member's credits")
    print("4. Verify the table updates after saving")
    
    print("=" * 50)
