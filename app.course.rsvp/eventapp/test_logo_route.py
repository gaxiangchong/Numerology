#!/usr/bin/env python3
"""
Add a test route to your app to verify logo display
"""

import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app

@app.route('/test-logo')
def test_logo():
    """Test route to verify logo display"""
    logo_path = os.path.join('static', 'images', 'logos', 'chinese-seal.png')
    
    if os.path.exists(logo_path):
        file_size = os.path.getsize(logo_path)
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Logo Test</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .logo-test {{ 
                    display: flex; 
                    align-items: center; 
                    gap: 20px; 
                    padding: 20px; 
                    border: 2px solid #007bff; 
                    border-radius: 10px; 
                    margin: 20px 0; 
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
                    background: #f8f9fa;
                }}
                .logo-image {{
                    width: 100%;
                    height: 100%;
                    object-fit: contain;
                    border-radius: 8px;
                }}
                .fallback-icon {{
                    display: none;
                    color: #007bff;
                    font-size: 24px;
                }}
                .info {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; }}
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
                    <h3>Current Logo Display</h3>
                    <p><strong>File:</strong> chinese-seal.png</p>
                    <p><strong>Size:</strong> {file_size:,} bytes</p>
                    <p><strong>Status:</strong> {'✅ Logo loaded successfully' if file_size > 0 else '❌ Logo file is empty'}</p>
                </div>
            </div>
            
            <div class="info">
                <h3>📋 Logo Information</h3>
                <p><strong>Path:</strong> {logo_path}</p>
                <p><strong>Characters:</strong> 卿合文化 (Qinghe Culture)</p>
                <p><strong>Expected:</strong> Red square with four Chinese characters</p>
                <p><strong>Fallback:</strong> If logo fails to load, graduation cap icon will appear</p>
            </div>
            
            <div class="info">
                <h3>🔧 How to Update</h3>
                <ol>
                    <li>Create your new logo with the four characters: 卿合文化</li>
                    <li>Save as PNG format</li>
                    <li>Replace the file at: <code>static/images/logos/chinese-seal.png</code></li>
                    <li>Refresh this page to see the changes</li>
                </ol>
            </div>
            
            <p><a href="/">← Back to App</a></p>
        </body>
        </html>
        '''
    else:
        return f'''
        <h1>❌ Logo Not Found</h1>
        <p>Logo file not found at: {logo_path}</p>
        <p>Please ensure the logo file exists at the correct location.</p>
        <p><a href="/">← Back to App</a></p>
        '''

if __name__ == '__main__':
    print("🎨 Logo Test Route Added")
    print("Visit: http://localhost:5000/test-logo")
    print("This will show you the current logo and help you test the update.")
