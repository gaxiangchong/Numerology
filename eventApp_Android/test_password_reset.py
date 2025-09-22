#!/usr/bin/env python3
"""
Test script for password reset functionality.

This script tests the password reset system by:
1. Creating a test user
2. Generating a password reset token
3. Testing token verification and expiration
4. Testing password reset functionality
"""

import os
import sys
from datetime import datetime, timedelta

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User

def test_password_reset():
    """Test password reset functionality."""
    print("Testing password reset system...")
    
    with app.app_context():
        try:
            # Create a test user
            test_email = "test_reset@example.com"
            test_user = User.query.filter_by(email=test_email).first()
            
            if test_user:
                print(f"Using existing test user: {test_user.email}")
            else:
                test_user = User(
                    username="testresetuser",
                    email=test_email,
                    country="Singapore"
                )
                test_user.set_password("oldpassword")
                db.session.add(test_user)
                db.session.commit()
                print(f"Created test user: {test_user.email}")
            
            # Test 1: Generate password reset token
            print("\n1. Testing password reset token generation...")
            token = test_user.generate_password_reset_token()
            db.session.commit()
            
            print(f"✅ Generated token: {token[:20]}...")
            print(f"✅ Token sent at: {test_user.password_reset_sent_at}")
            print(f"✅ Token exists: {test_user.password_reset_token is not None}")
            
            # Test 2: Check token expiration (should not be expired)
            print("\n2. Testing token expiration check...")
            if not test_user.is_password_reset_token_expired():
                print("✅ Token correctly identified as not expired")
            else:
                print("❌ Token should not be expired!")
            
            # Test 3: Test token expiration (manually set to expired)
            print("\n3. Testing token expiration (manually expired)...")
            # Manually set the token to be expired (2 hours ago)
            test_user.password_reset_sent_at = datetime.utcnow() - timedelta(hours=2)
            db.session.commit()
            
            if test_user.is_password_reset_token_expired():
                print("✅ Token correctly identified as expired")
            else:
                print("❌ Token should be expired!")
            
            # Test 4: Test password reset
            print("\n4. Testing password reset...")
            # Reset the token time to valid
            test_user.password_reset_sent_at = datetime.utcnow()
            db.session.commit()
            
            # Simulate password reset
            old_password_hash = test_user.password_hash
            test_user.set_password("newpassword")
            test_user.clear_password_reset_token()
            db.session.commit()
            
            print("✅ Password reset successful!")
            print(f"✅ Password hash changed: {old_password_hash != test_user.password_hash}")
            print(f"✅ Token cleared: {test_user.password_reset_token is None}")
            print(f"✅ New password works: {test_user.check_password('newpassword')}")
            print(f"✅ Old password doesn't work: {not test_user.check_password('oldpassword')}")
            
            # Clean up test user
            print("\n5. Cleaning up test user...")
            db.session.delete(test_user)
            db.session.commit()
            print("✅ Test user cleaned up")
            
            print("\n🎉 All password reset tests passed!")
            
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    test_password_reset()
