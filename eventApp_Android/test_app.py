#!/usr/bin/env python3
"""
Test script to debug Flask app issues
"""

import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing Flask app...")

try:
    from app import app
    print("✅ App imported successfully")
    
    # Check if app has routes
    print(f"✅ App has {len(app.url_map._rules)} routes")
    
    # List all routes
    print("Routes:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.rule} -> {rule.endpoint}")
    
    # Test the app
    with app.test_client() as client:
        response = client.get('/')
        print(f"✅ GET / returns status: {response.status_code}")
        if response.status_code != 200:
            print(f"❌ Error: {response.data.decode()}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
