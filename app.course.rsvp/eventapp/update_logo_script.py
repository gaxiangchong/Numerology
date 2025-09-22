#!/usr/bin/env python3
"""
Logo Update Script
This script helps you update the logo and provides instructions.
"""

import os
import sys
import shutil
from datetime import datetime

def update_logo_instructions():
    """Provide instructions for updating the logo."""
    print("🎨 Logo Update Instructions")
    print("=" * 40)
    
    logo_path = os.path.join('static', 'images', 'logos', 'chinese-seal.png')
    
    print(f"📁 Current logo location: {logo_path}")
    
    if os.path.exists(logo_path):
        # Get current file info
        current_size = os.path.getsize(logo_path)
        current_time = os.path.getmtime(logo_path)
        current_time_str = datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"📏 Current file size: {current_size:,} bytes")
        print(f"🕒 Last modified: {current_time_str}")
        
        # Create backup
        backup_path = f"{logo_path}.backup_{int(current_time)}"
        try:
            shutil.copy2(logo_path, backup_path)
            print(f"💾 Backup created: {backup_path}")
        except Exception as e:
            print(f"⚠️  Could not create backup: {e}")
    
    print("\n🔄 Steps to Update Logo:")
    print("1. Save your new logo as 'chinese-seal.png'")
    print("2. Replace the file at: static/images/logos/chinese-seal.png")
    print("3. The new logo should be:")
    print("   - Red square with four Chinese characters: 卿合文化")
    print("   - PNG format with transparent background")
    print("   - Recommended size: 48x48 pixels")
    print("   - Traditional Chinese seal appearance")
    
    print("\n🧪 Testing the Update:")
    print("1. Restart your app: python app.py")
    print("2. Visit: http://127.0.0.1:5001")
    print("3. The logo should now show your new design")
    print("4. If you still see the old logo, try Ctrl+F5 (hard refresh)")
    
    print("\n🚀 Deployment:")
    print("1. Commit changes: git add . && git commit -m 'Update logo'")
    print("2. Push to repository: git push origin main")
    print("3. Deploy to PythonAnywhere: Follow deployment guide")
    
    return True

def check_logo_file():
    """Check if the logo file has been updated."""
    logo_path = os.path.join('static', 'images', 'logos', 'chinese-seal.png')
    
    if os.path.exists(logo_path):
        current_size = os.path.getsize(logo_path)
        current_time = os.path.getmtime(logo_path)
        current_time_str = datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"\n📊 Current Logo Status:")
        print(f"   File: {logo_path}")
        print(f"   Size: {current_size:,} bytes")
        print(f"   Modified: {current_time_str}")
        
        # Check if file was recently modified (within last 5 minutes)
        now = datetime.now().timestamp()
        if (now - current_time) < 300:  # 5 minutes
            print("   ✅ Logo appears to have been recently updated!")
        else:
            print("   ⚠️  Logo file hasn't been updated recently")
        
        return True
    else:
        print(f"❌ Logo file not found: {logo_path}")
        return False

def create_test_page():
    """Create a test page to verify the logo update."""
    test_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Logo Update Test</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .logo-test { 
                display: flex; 
                align-items: center; 
                gap: 20px; 
                padding: 20px; 
                border: 2px solid #007bff; 
                border-radius: 10px; 
                margin: 20px 0; 
            }
            .logo-icon {
                width: 48px;
                height: 48px;
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
                overflow: hidden;
                background: #f8f9fa;
            }
            .logo-image {
                width: 100%;
                height: 100%;
                object-fit: contain;
                border-radius: 8px;
            }
            .fallback-icon {
                display: none;
                color: #007bff;
                font-size: 24px;
            }
            .info { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; }
        </style>
    </head>
    <body>
        <h1>🎨 Logo Update Test</h1>
        
        <div class="logo-test">
            <div class="logo-icon">
                <img src="/static/images/logos/chinese-seal.png?v=3" 
                     alt="卿合文化" 
                     class="logo-image" 
                     onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                <i class="fas fa-graduation-cap fallback-icon"></i>
            </div>
            <div>
                <h3>Updated Logo (v=3)</h3>
                <p>This should show your new logo design</p>
                <p>Characters: 卿合文化 (Qinghe Culture)</p>
            </div>
        </div>
        
        <div class="info">
            <h3>📋 Expected Logo Design</h3>
            <ul>
                <li>Red square background</li>
                <li>Four Chinese characters: 卿合文化</li>
                <li>Traditional seal appearance</li>
                <li>White or contrasting text color</li>
            </ul>
        </div>
        
        <div class="info">
            <h3>🔧 If Logo Doesn't Update</h3>
            <ol>
                <li>Make sure you replaced the file at: static/images/logos/chinese-seal.png</li>
                <li>Try hard refresh: Ctrl+F5</li>
                <li>Check browser cache settings</li>
                <li>Restart your Flask app</li>
            </ol>
        </div>
        
        <p><a href="/">← Back to App</a></p>
    </body>
    </html>
    '''
    
    with open('logo_update_test.html', 'w', encoding='utf-8') as f:
        f.write(test_html)
    
    print(f"📄 Test page created: logo_update_test.html")
    return True

if __name__ == '__main__':
    print("🎨 Logo Update Helper")
    print("=" * 30)
    
    # Show instructions
    update_logo_instructions()
    
    # Check current file
    check_logo_file()
    
    # Create test page
    create_test_page()
    
    print(f"\n🎯 Next Steps:")
    print("1. Replace the logo file with your new design")
    print("2. Restart your app: python app.py")
    print("3. Test the update at: http://127.0.0.1:5001")
    print("4. Use the test page to verify the logo")
