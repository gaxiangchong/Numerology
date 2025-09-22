#!/usr/bin/env python3
"""
Test script to verify logo update
"""

import os
import sys
from flask import Flask, render_template_string

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app

def test_logo_display():
    """Test that the logo displays correctly."""
    print("🎨 Testing logo display...")
    
    with app.app_context():
        try:
            # Check if logo file exists
            logo_path = os.path.join('static', 'images', 'logos', 'chinese-seal.png')
            if os.path.exists(logo_path):
                print(f"✅ Logo file found: {logo_path}")
                
                # Get file size
                file_size = os.path.getsize(logo_path)
                print(f"📏 Logo file size: {file_size} bytes")
                
                # Test logo in a simple HTML page
                test_html = f'''
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Logo Test</title>
                    <style>
                        .logo-test {{
                            display: flex;
                            align-items: center;
                            gap: 20px;
                            padding: 20px;
                            border: 1px solid #ccc;
                            margin: 20px;
                        }}
                        .logo-icon {{
                            width: 48px;
                            height: 48px;
                            border-radius: 12px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
                            overflow: hidden;
                        }}
                        .logo-image {{
                            width: 100%;
                            height: 100%;
                            object-fit: contain;
                            border-radius: 8px;
                        }}
                        .fallback-icon {{
                            display: none;
                            color: white;
                            font-size: 24px;
                        }}
                    </style>
                </head>
                <body>
                    <h1>🎨 Logo Test Page</h1>
                    <div class="logo-test">
                        <div class="logo-icon">
                            <img src="/static/images/logos/chinese-seal.png" 
                                 alt="卿合文化" 
                                 class="logo-image" 
                                 onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                            <i class="fas fa-graduation-cap fallback-icon"></i>
                        </div>
                        <div>
                            <h3>Current Logo</h3>
                            <p>File: chinese-seal.png</p>
                            <p>Size: {file_size} bytes</p>
                            <p>If you see a graduation cap, the logo image failed to load.</p>
                        </div>
                    </div>
                    <p><a href="/">← Back to App</a></p>
                </body>
                </html>
                '''
                
                return test_html
            else:
                print(f"❌ Logo file not found: {logo_path}")
                return f'''
                <h1>❌ Logo Not Found</h1>
                <p>Logo file not found at: {logo_path}</p>
                <p>Please ensure the logo file exists at the correct location.</p>
                <p><a href="/">← Back to App</a></p>
                '''
                
        except Exception as e:
            print(f"❌ Error testing logo: {e}")
            return f'''
            <h1>❌ Logo Test Error</h1>
            <p>Error: {str(e)}</p>
            <p><a href="/">← Back to App</a></p>
            '''

if __name__ == '__main__':
    print("🎨 Logo Test Script")
    print("=" * 30)
    
    # Test logo file
    logo_path = os.path.join('static', 'images', 'logos', 'chinese-seal.png')
    if os.path.exists(logo_path):
        print(f"✅ Logo file exists: {logo_path}")
        file_size = os.path.getsize(logo_path)
        print(f"📏 File size: {file_size} bytes")
        
        if file_size > 0:
            print("✅ Logo file has content")
        else:
            print("⚠️  Logo file is empty")
    else:
        print(f"❌ Logo file not found: {logo_path}")
        print("📁 Checking directory structure...")
        
        logos_dir = os.path.join('static', 'images', 'logos')
        if os.path.exists(logos_dir):
            print(f"✅ Logos directory exists: {logos_dir}")
            files = os.listdir(logos_dir)
            print(f"📁 Files in directory: {files}")
        else:
            print(f"❌ Logos directory not found: {logos_dir}")
    
    print("\n🎯 Next steps:")
    print("1. Update the logo file at static/images/logos/chinese-seal.png")
    print("2. Run your app: python app.py")
    print("3. Check the header to see the new logo")
    print("4. Test the fallback system by temporarily renaming the logo file")
