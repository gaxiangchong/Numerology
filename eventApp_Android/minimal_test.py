#!/usr/bin/env python3
"""
Minimal test to see if the app can start
"""

print("🚀 Starting minimal app test...")

try:
    print("📦 Importing app...")
    from app import app
    print("✅ App imported successfully!")
    
    print("🔧 Testing app context...")
    with app.app_context():
        print("✅ App context works!")
        
        # Test database
        from app import db
        print("✅ Database connection works!")
        
        # Test a simple query
        from app import User
        user_count = User.query.count()
        print(f"✅ Database query works! Found {user_count} users")
    
    print("🎉 App is ready to start!")
    print("🌐 You can now run: python app.py")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
