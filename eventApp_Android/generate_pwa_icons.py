#!/usr/bin/env python3
"""
Generate PWA icons from existing logo
This script creates multiple icon sizes required for PWA installation
"""

import os
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

def create_pwa_icons():
    """Generate PWA icons in various sizes"""
    
    # Create PWA icons directory
    pwa_dir = "static/images/pwa"
    os.makedirs(pwa_dir, exist_ok=True)
    
    # Icon sizes needed for PWA
    icon_sizes = [
        (16, 16), (32, 32), (48, 48), (72, 72), (96, 96), 
        (128, 128), (144, 144), (152, 152), (192, 192), 
        (256, 256), (384, 384), (512, 512)
    ]
    
    # Try to load existing logo
    logo_path = "static/images/logos/chinese-seal.png"
    
    if os.path.exists(logo_path):
        # Use existing logo
        base_image = Image.open(logo_path)
        print(f"Using existing logo: {logo_path}")
    else:
        # Create a simple logo if none exists
        base_image = create_simple_logo()
        print("Created simple logo")
    
    # Generate icons for each size
    for size in icon_sizes:
        width, height = size
        filename = f"icon-{width}x{height}.png"
        filepath = os.path.join(pwa_dir, filename)
        
        # Resize image
        icon = base_image.resize((width, height), Image.Resampling.LANCZOS)
        
        # Save icon
        icon.save(filepath, "PNG", optimize=True)
        print(f"Generated: {filename}")
    
    # Create browserconfig.xml for Windows tiles
    create_browserconfig()
    
    print(f"\nPWA icons generated successfully in {pwa_dir}/")
    print("You can now install the app on Android devices!")

def create_simple_logo():
    """Create a simple logo if none exists"""
    # Create a 512x512 base image
    img = Image.new('RGBA', (512, 512), (0, 123, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw a simple "NQ" logo
    try:
        # Try to use a system font
        font = ImageFont.truetype("arial.ttf", 200)
    except:
        try:
            font = ImageFont.load_default()
        except:
            font = None
    
    if font:
        # Draw "NQ" text
        text = "NQ"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (512 - text_width) // 2
        y = (512 - text_height) // 2
        
        draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    else:
        # Draw a simple circle if no font available
        draw.ellipse([100, 100, 412, 412], fill=(255, 255, 255, 255))
    
    return img

def create_browserconfig():
    """Create browserconfig.xml for Windows tiles"""
    browserconfig_content = '''<?xml version="1.0" encoding="utf-8"?>
<browserconfig>
    <msapplication>
        <tile>
            <square70x70logo src="/static/images/pwa/icon-72x72.png"/>
            <square150x150logo src="/static/images/pwa/icon-152x152.png"/>
            <square310x310logo src="/static/images/pwa/icon-384x384.png"/>
            <TileColor>#007bff</TileColor>
        </tile>
    </msapplication>
</browserconfig>'''
    
    with open("static/images/pwa/browserconfig.xml", "w") as f:
        f.write(browserconfig_content)
    
    print("Generated: browserconfig.xml")

if __name__ == "__main__":
    try:
        create_pwa_icons()
    except ImportError:
        print("PIL (Pillow) is required. Install it with: pip install Pillow")
    except Exception as e:
        print(f"Error generating icons: {e}")
        print("Creating simple fallback icons...")
        
        # Create simple fallback icons without PIL
        pwa_dir = "static/images/pwa"
        os.makedirs(pwa_dir, exist_ok=True)
        
        # Create a simple text file as placeholder
        with open(os.path.join(pwa_dir, "README.txt"), "w") as f:
            f.write("PWA icons need to be generated.\n")
            f.write("Run: python generate_pwa_icons.py\n")
            f.write("Or manually create icons in the required sizes.")
