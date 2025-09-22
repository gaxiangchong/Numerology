#!/usr/bin/env python3
"""
Test Gmail SMTP Connection
This script tests if we can connect to Gmail's SMTP servers.
"""

import socket
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_gmail_connection():
    """Test Gmail SMTP connection."""
    print("🔧 Testing Gmail SMTP Connection...")
    print("=" * 50)
    
    # Test 1: Basic network connectivity
    print("\n1️⃣ Testing network connectivity to Gmail...")
    try:
        # Test if we can reach Gmail's SMTP server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)  # 10 second timeout
        result = sock.connect_ex(('smtp.gmail.com', 587))
        sock.close()
        
        if result == 0:
            print("✅ Can reach smtp.gmail.com:587")
        else:
            print("❌ Cannot reach smtp.gmail.com:587")
            print("   This might be a firewall or network issue")
            return False
    except Exception as e:
        print(f"❌ Network test failed: {e}")
        return False
    
    # Test 2: SMTP connection
    print("\n2️⃣ Testing SMTP connection...")
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=30)
        server.starttls()
        print("✅ SMTP connection successful")
        server.quit()
        return True
    except Exception as e:
        print(f"❌ SMTP connection failed: {e}")
        return False

def test_with_credentials():
    """Test with actual credentials."""
    print("\n3️⃣ Testing with credentials...")
    
    # Read current .env file
    try:
        with open('.env', 'r') as f:
            content = f.read()
        
        # Extract credentials
        username = None
        password = None
        
        for line in content.split('\n'):
            if line.startswith('MAIL_USERNAME='):
                username = line.split('=', 1)[1].strip()
            elif line.startswith('MAIL_PASSWORD='):
                password = line.split('=', 1)[1].strip()
        
        if not username or not password:
            print("❌ Could not find credentials in .env file")
            return False
        
        print(f"📧 Username: {username}")
        print(f"🔑 Password: {'*' * len(password)}")
        
        # Test authentication
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587, timeout=30)
            server.starttls()
            server.login(username, password)
            print("✅ Authentication successful!")
            server.quit()
            return True
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False

def suggest_alternatives():
    """Suggest alternative solutions."""
    print("\n🔄 Alternative Solutions:")
    print("=" * 50)
    
    print("\n1️⃣ Check Gmail App Password:")
    print("   • Make sure 2-Step Verification is enabled")
    print("   • Create a new App Password")
    print("   • Use the 16-character password (no spaces)")
    
    print("\n2️⃣ Try different Gmail settings:")
    print("   • Use port 465 with SSL instead of 587 with TLS")
    print("   • Check if your network blocks SMTP ports")
    
    print("\n3️⃣ Use a different email provider:")
    print("   • Yahoo Mail (easier setup)")
    print("   • Outlook with proper App Password")
    print("   • Custom SMTP server")
    
    print("\n4️⃣ Network/Firewall issues:")
    print("   • Check if your firewall blocks port 587")
    print("   • Try from a different network")
    print("   • Contact your IT administrator")

def main():
    print("🧪 Gmail SMTP Connection Test")
    print("=" * 50)
    
    # Test basic connection
    if not test_gmail_connection():
        suggest_alternatives()
        return False
    
    # Test with credentials
    if not test_with_credentials():
        suggest_alternatives()
        return False
    
    print("\n🎉 Gmail connection is working!")
    print("The issue might be in the Flask app configuration.")
    return True

if __name__ == "__main__":
    main()
