#!/usr/bin/env python3
"""
Email configuration test script.

This script tests the email configuration and sends a test email.
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, send_email

def test_email_configuration():
    """Test email configuration and send a test email."""
    print("🔧 Testing Email Configuration...")
    print("=" * 50)
    
    with app.app_context():
        # Check configuration
        print(f"MAIL_SERVER: {app.config.get('MAIL_SERVER', 'Not set')}")
        print(f"MAIL_PORT: {app.config.get('MAIL_PORT', 'Not set')}")
        print(f"MAIL_USE_TLS: {app.config.get('MAIL_USE_TLS', 'Not set')}")
        print(f"MAIL_USERNAME: {app.config.get('MAIL_USERNAME', 'Not set')}")
        print(f"MAIL_PASSWORD: {'Set' if app.config.get('MAIL_PASSWORD') else 'Not set'}")
        print()
        
        # Check if email is configured
        if not app.config.get('MAIL_USERNAME') or not app.config.get('MAIL_PASSWORD'):
            print("❌ Email configuration is incomplete!")
            print()
            print("To fix this:")
            print("1. Create a .env file in the eventapp directory")
            print("2. Copy the content from env_example.txt")
            print("3. Fill in your email credentials")
            print()
            print("For Gmail:")
            print("- Enable 2-factor authentication")
            print("- Generate an App Password")
            print("- Use the App Password (not your regular password)")
            print()
            return False
        
        # Test email sending
        test_email = input("Enter your email address to send a test email: ").strip()
        if not test_email:
            print("No email provided. Skipping test email.")
            return True
        
        print(f"\n📧 Sending test email to {test_email}...")
        
        subject = "EventApp - Email Configuration Test"
        body = f"""Hello!

This is a test email from EventApp to verify that email configuration is working correctly.

Test sent at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

If you receive this email, your email configuration is working properly!

Best regards,
EventApp Team"""

        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #007bff;">EventApp - Email Configuration Test</h2>
                <p>Hello!</p>
                <p>This is a test email from EventApp to verify that email configuration is working correctly.</p>
                
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p><strong>Test sent at:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                
                <p>If you receive this email, your email configuration is working properly!</p>
                
                <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                <p style="color: #666; font-size: 14px;">
                    Best regards,<br>
                    EventApp Team
                </p>
            </div>
        </body>
        </html>
        """
        
        success = send_email(test_email, subject, body, html_body)
        
        if success:
            print("✅ Test email sent successfully!")
            print("Check your inbox (and spam folder) for the test email.")
        else:
            print("❌ Failed to send test email.")
            print("Check the error messages above for troubleshooting.")
        
        return success

if __name__ == '__main__':
    test_email_configuration()
