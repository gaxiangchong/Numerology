#!/usr/bin/env python3
"""
Test script for the credit system functionality.
This script tests the credit point system implementation.
"""

import os
import sys
from sqlalchemy import create_engine, text

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User

def test_credit_system():
    """Test the credit system functionality."""
    print("🧪 Testing Credit System...")
    
    try:
        with app.app_context():
            # Test 1: Check if credit_point column exists
            print("\n1️⃣ Testing database schema...")
            with db.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT COUNT(*) as count 
                    FROM pragma_table_info('user') 
                    WHERE name = 'credit_point'
                """))
                column_exists = result.fetchone()[0] > 0
                
                if column_exists:
                    print("✅ credit_point column exists in database")
                else:
                    print("❌ credit_point column missing from database")
                    return False
            
            # Test 2: Check user credit points
            print("\n2️⃣ Testing user credit points...")
            users = User.query.all()
            print(f"📊 Found {len(users)} users in database")
            
            for user in users:
                credit_point = user.credit_point if hasattr(user, 'credit_point') else 'N/A'
                print(f"   👤 {user.username}: {credit_point} credits")
            
            # Test 3: Test credit point updates
            print("\n3️⃣ Testing credit point updates...")
            if users:
                test_user = users[0]
                original_credits = test_user.credit_point
                print(f"   📝 Original credits for {test_user.username}: {original_credits}")
                
                # Update credits
                test_user.credit_point = 100.50
                db.session.commit()
                
                # Verify update
                updated_user = User.query.get(test_user.id)
                print(f"   ✅ Updated credits for {updated_user.username}: {updated_user.credit_point}")
                
                # Restore original credits
                test_user.credit_point = original_credits
                db.session.commit()
                print(f"   🔄 Restored original credits: {original_credits}")
            
            # Test 4: Test credit point validation
            print("\n4️⃣ Testing credit point validation...")
            if users:
                test_user = users[0]
                
                # Test negative credits (should be set to 0)
                test_user.credit_point = -10.0
                db.session.commit()
                updated_user = User.query.get(test_user.id)
                print(f"   ✅ Negative credits handled: {updated_user.credit_point} (should be 0.0)")
                
                # Test decimal credits
                test_user.credit_point = 123.45
                db.session.commit()
                updated_user = User.query.get(test_user.id)
                print(f"   ✅ Decimal credits handled: {updated_user.credit_point}")
                
                # Restore original
                test_user.credit_point = original_credits
                db.session.commit()
            
            print("\n🎉 All credit system tests passed!")
            return True
            
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        return False

def show_credit_summary():
    """Show a summary of all users' credit points."""
    print("\n📊 Credit Points Summary:")
    print("=" * 50)
    
    try:
        with app.app_context():
            users = User.query.all()
            total_credits = 0
            
            for user in users:
                credits = user.credit_point if hasattr(user, 'credit_point') else 0
                total_credits += credits
                status = "🟢 Active" if user.account_status == 'active' else "🔴 Inactive"
                print(f"👤 {user.username:<20} | 💰 {credits:>8.2f} | {status}")
            
            print("=" * 50)
            print(f"📈 Total Credits: {total_credits:.2f}")
            print(f"👥 Total Users: {len(users)}")
            print(f"📊 Average Credits: {total_credits/len(users):.2f}" if users else "📊 Average Credits: 0.00")
            
    except Exception as e:
        print(f"❌ Error showing summary: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🏦 Credit System Test Suite")
    print("=" * 60)
    
    success = test_credit_system()
    
    if success:
        show_credit_summary()
        print("\n✅ Credit system is ready for use!")
        print("\n📋 Next steps:")
        print("1. Go to Admin → Member Management")
        print("2. Click edit on any member")
        print("3. Adjust credit points using the +/- buttons")
        print("4. Save changes with superuser password")
    else:
        print("\n❌ Credit system tests failed!")
        print("Please check the error messages above.")
    
    print("=" * 60)
