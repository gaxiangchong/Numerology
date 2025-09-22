#!/usr/bin/env python3
"""
Icon Generator for Numerology PWA
Creates placeholder icons in various sizes for the PWA manifest
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, filename):
    """Create a simple icon with numerology theme"""
    # Create a new image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Background circle with blue gradient effect
    margin = size // 10
    draw.ellipse([margin, margin, size-margin, size-margin], 
                fill=(59, 130, 246, 255), outline=(37, 99, 235, 255), width=2)
    
    # Draw a simple "N" for Numerology
    try:
        # Try to use a system font
        font_size = size // 3
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Calculate text position
    text = "N"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - 2
    
    # Draw the text
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    
    # Add some decorative elements
    if size >= 96:
        # Add small dots around the circle
        dot_size = size // 20
        for angle in [45, 135, 225, 315]:
            import math
            center_x = size // 2
            center_y = size // 2
            radius = (size - margin) // 2 + dot_size
            dot_x = center_x + radius * math.cos(math.radians(angle))
            dot_y = center_y + radius * math.sin(math.radians(angle))
            draw.ellipse([dot_x-dot_size//2, dot_y-dot_size//2, 
                         dot_x+dot_size//2, dot_y+dot_size//2], 
                        fill=(255, 255, 255, 200))
    
    # Save the image
    img.save(filename, 'PNG')
    print(f"Created {filename} ({size}x{size})")

def main():
    """Generate all required icon sizes"""
    icon_sizes = [72, 96, 128, 144, 152, 192, 384, 512]
    
    # Ensure icons directory exists
    os.makedirs('icons', exist_ok=True)
    
    for size in icon_sizes:
        filename = f'icons/icon-{size}x{size}.png'
        create_icon(size, filename)
    
    print("All icons generated successfully!")
    print("Note: These are placeholder icons. Replace with your actual app icon design.")

if __name__ == "__main__":
    main()
