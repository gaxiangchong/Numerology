#!/usr/bin/env python3
"""
Fix Network Email Issues
This script tries different email configurations to work around network restrictions.
"""

import socket
import smtplib

def test_port(host, port, timeout=5):
    """Test if a port is accessible."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def test_email_ports():
    """Test different email ports."""
    print("🔧 Testing Email Ports...")
    print("=" * 50)
    
    # Common email ports
    ports_to_test = [
        ('smtp.gmail.com', 587, 'Gmail TLS'),
        ('smtp.gmail.com', 465, 'Gmail SSL'),
        ('smtp-mail.outlook.com', 587, 'Outlook TLS'),
        ('smtp-mail.outlook.com', 465, 'Outlook SSL'),
        ('smtp.mail.yahoo.com', 587, 'Yahoo TLS'),
        ('smtp.mail.yahoo.com', 465, 'Yahoo SSL'),
    ]
    
    working_ports = []
    
    for host, port, description in ports_to_test:
        print(f"Testing {description} ({host}:{port})...", end=" ")
        if test_port(host, port):
            print("✅ Working")
            working_ports.append((host, port, description))
        else:
            print("❌ Blocked")
    
    return working_ports

def create_working_config(host, port, description):
    """Create configuration for working email server."""
    print(f"\n📧 Creating configuration for {description}...")
    
    if 'gmail' in host.lower():
        username = 'noblequest.edu@gmail.com'
        password = 'uyau xvwk agny pnlz'  # Your Gmail app password
        use_tls = port == 587
        use_ssl = port == 465
    elif 'outlook' in host.lower():
        username = 'noblequest.edu@outlook.com'
        password = 'cehmjputdyfikvzc'  # Your Outlook app password
        use_tls = port == 587
        use_ssl = port == 465
    elif 'yahoo' in host.lower():
        username = 'noblequest.edu@yahoo.com'
        password = 'your_yahoo_app_password'  # You'll need to create this
        use_tls = port == 587
        use_ssl = port == 465
    
    config = f"""# EventApp Environment Configuration
# Working email configuration for {description}

# Flask Configuration
SECRET_KEY=ff51f8a92aaa245c385f100331f943ed1dd42a2726d4546578ef5f787a980635
FLASK_ENV=development
DATABASE_URL=sqlite:///eventapp.db

# Email Configuration
MAIL_SERVER={host}
MAIL_PORT={port}
MAIL_USE_TLS={str(use_tls).lower()}
MAIL_USE_SSL={str(use_ssl).lower()}
MAIL_USERNAME={username}
MAIL_PASSWORD={password}

# App Configuration
APP_NAME=EventApp
"""
    
    with open('.env', 'w') as f:
        f.write(config)
    
    print(f"✅ Configuration saved for {description}")
    return True

def try_alternative_solutions():
    """Try alternative solutions."""
    print("\n🔄 Alternative Solutions:")
    print("=" * 50)
    
    print("\n1️⃣ Use a different network:")
    print("   • Try from your home network")
    print("   • Use mobile hotspot")
    print("   • Try from a different location")
    
    print("\n2️⃣ Contact your IT administrator:")
    print("   • Ask them to unblock SMTP ports")
    print("   • Request access to email servers")
    print("   • Ask for corporate email configuration")
    
    print("\n3️⃣ Use a different email service:")
    print("   • Try Yahoo Mail")
    print("   • Use a different Gmail account")
    print("   • Consider using a different email provider")
    
    print("\n4️⃣ Temporary workaround:")
    print("   • Disable email verification temporarily")
    print("   • Use the app without email features")
    print("   • Fix email later when network allows")

def main():
    print("🔧 Network Email Configuration Fix")
    print("=" * 50)
    
    # Test different ports
    working_ports = test_email_ports()
    
    if working_ports:
        print(f"\n✅ Found {len(working_ports)} working email configuration(s):")
        for i, (host, port, description) in enumerate(working_ports, 1):
            print(f"   {i}. {description} ({host}:{port})")
        
        # Use the first working configuration
        host, port, description = working_ports[0]
        create_working_config(host, port, description)
        
        print(f"\n🎉 Using {description} configuration!")
        print("📋 Next steps:")
        print("1. Test the configuration: python test_email_config.py")
        print("2. Try registering a new user")
        print("3. Check if verification emails are sent")
        
        return True
    else:
        print("\n❌ No working email ports found.")
        print("All common email ports are blocked by your network.")
        try_alternative_solutions()
        return False

if __name__ == "__main__":
    success = main()
    
    if not success:
        print("\n💡 Recommendation:")
        print("Since email ports are blocked, you might want to:")
        print("1. Use the app without email verification")
        print("2. Try from a different network")
        print("3. Contact your IT administrator")
    
    print("=" * 50)
