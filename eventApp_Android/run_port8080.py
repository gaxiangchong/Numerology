#!/usr/bin/env python3
"""
Run EventApp on port 8080 for Android testing
"""

import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the app
from app import app

if __name__ == '__main__':
    print("=" * 50)
    print("  EventApp - Android PWA (Port 8080)")
    print("=" * 50)
    print()
    print("Your IP address: 192.168.68.116")
    print()
    print("Android access URLs:")
    print("- Real device: http://192.168.68.116:8080")
    print("- Emulator: http://10.0.2.2:8080")
    print()
    print("Starting EventApp on port 8080...")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    print()
    
    # Run the app on port 8080
    app.run(host='0.0.0.0', debug=True, port=8080)
