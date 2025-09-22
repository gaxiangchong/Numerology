#!/usr/bin/env python3
"""
Test script to verify the app can start without errors
"""

def test_app_start():
    """Test if the app can start without errors"""
    print("🚀 Testing App Startup")
    print("=" * 30)
    
    try:
        print("📦 Importing Flask app...")
        from app import app
        print("✅ App imported successfully!")
        
        print("🔧 Testing app configuration...")
        print(f"   - Secret Key: {'✅ Set' if app.config.get('SECRET_KEY') else '❌ Missing'}")
        print(f"   - Database URI: {'✅ Set' if app.config.get('SQLALCHEMY_DATABASE_URI') else '❌ Missing'}")
        print(f"   - Stripe Key: {'✅ Set' if app.config.get('STRIPE_SECRET_KEY') else '❌ Missing'}")
        
        print("🗄️ Testing database connection...")
        with app.app_context():
            from app import db
            # Test a simple query
            result = db.engine.execute("SELECT 1").fetchone()
            print("✅ Database connection successful!")
        
        print("🎯 Testing template context...")
        with app.app_context():
            # Test if helper functions are available
            from app import get_membership_grade_info
            grade_info = get_membership_grade_info('Classic')
            print(f"✅ Helper functions working: {grade_info['name']}")
        
        print("\n🎉 All tests passed! The app should start successfully.")
        print("🌐 You can now start the app with: python app.py")
        print("🔗 Then visit: http://localhost:5001")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("🔧 Please check the error above and fix any issues.")
        return False
    
    return True

if __name__ == "__main__":
    test_app_start()
