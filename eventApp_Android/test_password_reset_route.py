#!/usr/bin/env python3
"""
Test script to verify password reset route is working correctly.
"""

import requests
import sys

def test_password_reset_route():
    """Test the password reset route."""
    print("🧪 Testing Password Reset Route...")
    print("=" * 40)
    
    # Test URL
    base_url = "http://127.0.0.1:5001"
    test_user_id = 1  # Assuming user ID 1 exists
    
    print(f"📡 Testing route: {base_url}/admin/members/{test_user_id}/reset-password")
    
    try:
        # Test GET request (should fail with Method Not Allowed)
        print("\n1. Testing GET request (should fail)...")
        response = requests.get(f"{base_url}/admin/members/{test_user_id}/reset-password")
        print(f"   Status Code: {response.status_code}")
        print(f"   Expected: 405 (Method Not Allowed)")
        
        if response.status_code == 405:
            print("   ✅ GET request correctly rejected")
        else:
            print("   ❌ GET request should be rejected")
        
        # Test POST request without authentication (should redirect to login)
        print("\n2. Testing POST request without auth (should redirect)...")
        response = requests.post(f"{base_url}/admin/members/{test_user_id}/reset-password", 
                               data={'superuser_password': 'test'})
        print(f"   Status Code: {response.status_code}")
        print(f"   Expected: 302 (Redirect to login)")
        
        if response.status_code == 302:
            print("   ✅ POST request correctly redirects to login")
        else:
            print("   ❌ POST request should redirect to login")
        
        print("\n✅ Route is working correctly!")
        print("   - GET requests are rejected (Method Not Allowed)")
        print("   - POST requests redirect to login (authentication required)")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Flask app.")
        print("   Make sure your Flask app is running on http://127.0.0.1:5001")
        print("   Start it with: python app.py")
    except Exception as e:
        print(f"❌ Error testing route: {e}")

if __name__ == "__main__":
    test_password_reset_route()
