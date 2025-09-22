#!/usr/bin/env python3
"""
Test script for QR code attendance system
This script helps you test the QR code functionality locally
"""

from app import app, db, User, Event, RSVP
from datetime import datetime, timedelta
import uuid

def test_qr_system():
    """Test the QR code system functionality"""
    with app.app_context():
        print("🔍 Testing QR Code Attendance System")
        print("=" * 50)
        
        # Check if we have an admin user
        admin_user = User.query.filter_by(is_admin=True).first()
        if not admin_user:
            print("❌ No admin user found. Please create one first.")
            print("   Run: python setup_admin.py")
            return
        
        print(f"✅ Admin user found: {admin_user.username} ({admin_user.email})")
        
        # Check if we have events
        events = Event.query.all()
        if not events:
            print("❌ No events found. Please create some events first.")
            return
        
        print(f"✅ Found {len(events)} events")
        
        # Check for RSVPs with QR codes
        rsvps_with_qr = RSVP.query.filter(RSVP.qr_code.isnot(None)).all()
        print(f"✅ Found {len(rsvps_with_qr)} RSVPs with QR codes")
        
        if rsvps_with_qr:
            print("\n📱 QR Codes Available for Testing:")
            print("-" * 40)
            for rsvp in rsvps_with_qr[:5]:  # Show first 5
                print(f"Event: {rsvp.event.name}")
                print(f"Attendee: {rsvp.attendee.display_name}")
                print(f"QR Code: {rsvp.qr_code}")
                print(f"Status: {rsvp.status}")
                print(f"Checked In: {'Yes' if rsvp.checked_in else 'No'}")
                if rsvp.checked_in_at:
                    print(f"Checked In At: {rsvp.checked_in_at}")
                print("-" * 40)
        
        print("\n🌐 Testing Instructions:")
        print("1. Open your browser and go to: http://localhost:5001")
        print("2. Login as admin user")
        print("3. Go to 'Check-In' in the navigation menu")
        print("4. Enter one of the QR codes above to test verification")
        print("5. Check if the attendee details are displayed correctly")
        
        print("\n📋 Available Test QR Codes:")
        for i, rsvp in enumerate(rsvps_with_qr[:3], 1):
            print(f"{i}. {rsvp.qr_code} (Event: {rsvp.event.name})")

if __name__ == "__main__":
    test_qr_system()
