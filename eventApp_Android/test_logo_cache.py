#!/usr/bin/env python3
"""
Test script to help with logo cache issues
"""

import os
import sys
import time

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_logo_cache():
    """Test logo file and provide cache-busting solutions."""
    print("🔄 Logo Cache Test")
    print("=" * 30)
    
    logo_path = os.path.join('static', 'images', 'logos', 'chinese-seal.png')
    
    if os.path.exists(logo_path):
        # Get file modification time
        mod_time = os.path.getmtime(logo_path)
        mod_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mod_time))
        file_size = os.path.getsize(logo_path)
        
        print(f"✅ Logo file found: {logo_path}")
        print(f"📏 File size: {file_size:,} bytes")
        print(f"🕒 Last modified: {mod_time_str}")
        
        # Create cache-busting URL
        cache_buster = int(mod_time)
        logo_url = f"/static/images/logos/chinese-seal.png?v={cache_buster}"
        
        print(f"\n🔧 Cache-busting URL: {logo_url}")
        
        # Create test HTML
        test_html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Logo Cache Test</title>
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
                .cache-solutions {{ background: #fff3cd; padding: 15px; border-radius: 5px; margin: 10px 0; border: 1px solid #ffeaa7; }}
            </style>
        </head>
        <body>
            <h1>🔄 Logo Cache Test</h1>
            
            <div class="logo-test">
                <div class="logo-icon">
                    <img src="{logo_url}" 
                         alt="卿合文化" 
                         class="logo-image" 
                         onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                    <i class="fas fa-graduation-cap fallback-icon"></i>
                </div>
                <div>
                    <h3>Current Logo (Cache-Busted)</h3>
                    <p><strong>File:</strong> chinese-seal.png</p>
                    <p><strong>Size:</strong> {file_size:,} bytes</p>
                    <p><strong>Modified:</strong> {mod_time_str}</p>
                    <p><strong>Cache Buster:</strong> v={cache_buster}</p>
                </div>
            </div>
            
            <div class="cache-solutions">
                <h3>🚀 Quick Cache Solutions</h3>
                <ol>
                    <li><strong>Hard Refresh:</strong> Press <code>Ctrl + F5</code> (Windows) or <code>Cmd + Shift + R</code> (Mac)</li>
                    <li><strong>Incognito Mode:</strong> Open a new incognito/private window</li>
                    <li><strong>Clear Cache:</strong> Press <code>Ctrl + Shift + Delete</code> and clear browsing data</li>
                    <li><strong>Developer Tools:</strong> Right-click → Inspect → Network tab → Disable cache</li>
                </ol>
            </div>
            
            <div class="info">
                <h3>📋 Logo Information</h3>
                <p><strong>Path:</strong> {logo_path}</p>
                <p><strong>Characters:</strong> 卿合文化 (Qinghe Culture)</p>
                <p><strong>Expected:</strong> Red square with four Chinese characters</p>
                <p><strong>Cache Buster:</strong> Added ?v={cache_buster} to force reload</p>
            </div>
            
            <div class="info">
                <h3>🔧 Permanent Fix</h3>
                <p>The template has been updated with cache-busting parameter.</p>
                <p>If you still see the old logo, try the solutions above.</p>
            </div>
            
            <p><a href="/">← Back to App</a></p>
        </body>
        </html>
        '''
        
        # Save test HTML
        with open('logo_cache_test.html', 'w', encoding='utf-8') as f:
            f.write(test_html)
        
        print(f"\n📄 Test HTML created: logo_cache_test.html")
        print(f"🌐 Open in browser: file://{os.path.abspath('logo_cache_test.html')}")
        
        return test_html
    else:
        print(f"❌ Logo file not found: {logo_path}")
        return None

if __name__ == '__main__':
    test_logo_cache()
