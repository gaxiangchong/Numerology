#!/usr/bin/env python3
"""
Create Android launcher icons for EventApp WebView
"""

import os
from PIL import Image, ImageDraw
import sys

def create_launcher_icons():
    """Create launcher icons in various sizes"""
    
    # Icon sizes for different densities
    icon_sizes = {
        'mipmap-mdpi': 48,
        'mipmap-hdpi': 72,
        'mipmap-xhdpi': 96,
        'mipmap-xxhdpi': 144,
        'mipmap-xxxhdpi': 192
    }
    
    # Create directories if they don't exist
    for density in icon_sizes.keys():
        os.makedirs(f'app/src/main/res/{density}', exist_ok=True)
    
    # Create a simple EventApp icon
    def create_icon(size, is_round=False):
        """Create an icon with EventApp branding"""
        # Create a square image
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Background circle
        margin = size // 8
        draw.ellipse([margin, margin, size-margin, size-margin], 
                    fill=(33, 150, 243, 255))  # Blue background
        
        # Add "E" for EventApp
        font_size = size // 2
        # Simple "E" using rectangles
        bar_width = size // 8
        bar_length = size // 2
        
        # Vertical bar
        draw.rectangle([size//2 - bar_width//2, size//4, 
                       size//2 + bar_width//2, size*3//4], fill='white')
        
        # Top horizontal bar
        draw.rectangle([size//2 - bar_length//2, size//4, 
                       size//2 + bar_length//2, size//4 + bar_width], fill='white')
        
        # Middle horizontal bar
        draw.rectangle([size//2 - bar_length//2, size//2 - bar_width//2, 
                       size//2 + bar_length//2, size//2 + bar_width//2], fill='white')
        
        # Bottom horizontal bar
        draw.rectangle([size//2 - bar_length//2, size*3//4 - bar_width, 
                       size//2 + bar_length//2, size*3//4], fill='white')
        
        if is_round:
            # For round icons, we can add a subtle border
            border_width = size // 32
            draw.ellipse([border_width, border_width, size-border_width, size-border_width], 
                        outline=(255, 255, 255, 100), width=border_width)
        
        return img
    
    # Create regular launcher icons
    for density, size in icon_sizes.items():
        icon = create_icon(size, is_round=False)
        icon.save(f'app/src/main/res/{density}/ic_launcher.png')
        print(f"✅ Created {density}/ic_launcher.png ({size}x{size})")
    
    # Create round launcher icons
    for density, size in icon_sizes.items():
        icon = create_icon(size, is_round=True)
        icon.save(f'app/src/main/res/{density}/ic_launcher_round.png')
        print(f"✅ Created {density}/ic_launcher_round.png ({size}x{size})")
    
    print("\n🎉 All launcher icons created successfully!")
    print("📱 Icons are ready for Android Studio")

if __name__ == "__main__":
    try:
        create_launcher_icons()
    except ImportError:
        print("❌ PIL (Pillow) not found. Installing...")
        os.system("pip install Pillow")
        print("✅ Pillow installed. Please run the script again.")
    except Exception as e:
        print(f"❌ Error creating icons: {e}")
        sys.exit(1)
