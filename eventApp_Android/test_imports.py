#!/usr/bin/env python3
"""
Test script to check if all imports work correctly
"""

def test_imports():
    """Test all imports one by one"""
    print("🔍 Testing imports...")
    
    try:
        print("📦 Testing Flask...")
        from flask import Flask
        print("✅ Flask imported successfully")
        
        print("📦 Testing Flask-SQLAlchemy...")
        from flask_sqlalchemy import SQLAlchemy
        print("✅ Flask-SQLAlchemy imported successfully")
        
        print("📦 Testing Flask-Login...")
        from flask_login import LoginManager
        print("✅ Flask-Login imported successfully")
        
        print("📦 Testing Stripe...")
        import stripe
        print("✅ Stripe imported successfully")
        
        print("📦 Testing QRCode...")
        import qrcode
        print("✅ QRCode imported successfully")
        
        print("📦 Testing Pillow...")
        from PIL import Image
        print("✅ Pillow imported successfully")
        
        print("📦 Testing dotenv...")
        from dotenv import load_dotenv
        print("✅ dotenv imported successfully")
        
        print("\n🎉 All imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

if __name__ == "__main__":
    test_imports()
