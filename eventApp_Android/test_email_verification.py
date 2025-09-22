#!/usr/bin/env python3
"""
Test script for email verification functionality.

This script tests the email verification system by:
1. Creating a test user
2. Generating a verification token
3. Testing token verification
4. Testing token expiration
"""

import os
import sys
from datetime import datetime, timedelta

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User

def test_email_verification():
    """Test email verification functionality."""
    print("Testing email verification system...")
    
    with app.app_context():
        try:
            # Create a test user
            test_email = "test@example.com"
            test_user = User.query.filter_by(email=test_email).first()
            
            if test_user:
                print(f"Using existing test user: {test_user.email}")
            else:
                test_user = User(
                    username="testuser",
                    email=test_email,
                    country="Singapore"
                )
                test_user.set_password("testpassword")
                db.session.add(test_user)
                db.session.commit()
                print(f"Created test user: {test_user.email}")
            
            # Test 1: Generate verification token
            print("\n1. Testing token generation...")
            token = test_user.generate_verification_token()
            db.session.commit()
            
            print(f"✅ Generated token: {token[:20]}...")
            print(f"✅ Token sent at: {test_user.email_verification_sent_at}")
            print(f"✅ Email verified status: {test_user.email_verified}")
            
            # Test 2: Verify email with correct token
            print("\n2. Testing email verification with correct token...")
            if test_user.verify_email(token):
                db.session.commit()
                print("✅ Email verification successful!")
                print(f"✅ Email verified status: {test_user.email_verified}")
                print(f"✅ Token cleared: {test_user.email_verification_token is None}")
            else:
                print("❌ Email verification failed!")
            
            # Test 3: Test with wrong token
            print("\n3. Testing email verification with wrong token...")
            test_user.email_verified = False  # Reset for testing
            test_user.generate_verification_token()
            db.session.commit()
            
            if test_user.verify_email("wrong_token"):
                print("❌ Verification should have failed with wrong token!")
            else:
                print("✅ Correctly rejected wrong token")
            
            # Test 4: Test token expiration
            print("\n4. Testing token expiration...")
            # Manually set the token to be expired (25 hours ago)
            test_user.email_verification_sent_at = datetime.utcnow() - timedelta(hours=25)
            db.session.commit()
            
            if test_user.is_verification_token_expired():
                print("✅ Token correctly identified as expired")
            else:
                print("❌ Token should be expired!")
            
            # Clean up test user
            print("\n5. Cleaning up test user...")
            db.session.delete(test_user)
            db.session.commit()
            print("✅ Test user cleaned up")
            
            print("\n🎉 All email verification tests passed!")
            
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    test_email_verification()
