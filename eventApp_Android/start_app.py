#!/usr/bin/env python3
"""
Simple app startup script with error handling
"""

import sys
import traceback

def start_app():
    """Start the Flask app with error handling"""
    print("🚀 Starting Noble Quest Event App...")
    print("=" * 40)
    
    try:
        print("📦 Importing app...")
        from app import app
        
        print("✅ App imported successfully!")
        print("🌐 Starting Flask development server...")
        print("🔗 App will be available at: http://localhost:5001")
        print("⏹️  Press Ctrl+C to stop the server")
        print("-" * 40)
        
        # Start the app
        app.run(debug=True, port=5001, host='0.0.0.0')
        
    except KeyboardInterrupt:
        print("\n⏹️  Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting app: {e}")
        print("\n🔍 Full error details:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    start_app()
