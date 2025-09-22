#!/usr/bin/env python3
"""
Screenshot Generator for PWA
Creates placeholder screenshots for the PWA manifest
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_screenshot(width, height, filename, is_mobile=False):
    """Create a placeholder screenshot"""
    # Create a new image
    img = Image.new('RGB', (width, height), (26, 26, 26))  # Dark background
    draw = ImageDraw.Draw(img)
    
    # Add a header bar
    header_height = height // 8
    draw.rectangle([0, 0, width, header_height], fill=(59, 130, 246, 255))
    
    # Add app title
    try:
        font_size = width // 20
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    title = "Numerology Analysis Tool"
    bbox = draw.textbbox((0, 0), title, font=font)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    y = header_height // 4
    
    draw.text((x, y), title, fill=(255, 255, 255, 255), font=font)
    
    # Add some content areas
    content_y = header_height + 20
    content_height = (height - header_height - 40) // 3
    
    # Main content area
    draw.rectangle([20, content_y, width-20, content_y + content_height], 
                  fill=(31, 41, 55, 255), outline=(75, 85, 99, 255))
    
    # Add some text content
    content_text = "Enter your license plate, phone number, or any combination"
    try:
        content_font_size = width // 25
        content_font = ImageFont.truetype("arial.ttf", content_font_size)
    except:
        content_font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), content_text, font=content_font)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    y = content_y + content_height // 2
    
    draw.text((x, y), content_text, fill=(229, 231, 235, 255), font=content_font)
    
    # Add feature boxes
    box_y = content_y + content_height + 20
    box_width = (width - 60) // 2
    box_height = content_height
    
    # Feature box 1
    draw.rectangle([20, box_y, 20 + box_width, box_y + box_height], 
                  fill=(31, 41, 55, 255), outline=(75, 85, 99, 255))
    
    # Feature box 2
    draw.rectangle([40 + box_width, box_y, width-20, box_y + box_height], 
                  fill=(31, 41, 55, 255), outline=(75, 85, 99, 255))
    
    # Add feature text
    feature_text = "Advanced Analysis" if is_mobile else "Energy Charts"
    bbox = draw.textbbox((0, 0), feature_text, font=content_font)
    text_width = bbox[2] - bbox[0]
    x1 = 20 + (box_width - text_width) // 2
    x2 = 40 + box_width + (box_width - text_width) // 2
    y = box_y + box_height // 2
    
    draw.text((x1, y), feature_text, fill=(229, 231, 235, 255), font=content_font)
    draw.text((x2, y), "Personalized Insights", fill=(229, 231, 235, 255), font=content_font)
    
    # Save the image
    img.save(filename, 'PNG')
    print(f"Created {filename} ({width}x{height})")

def main():
    """Generate screenshot placeholders"""
    # Ensure screenshots directory exists
    os.makedirs('screenshots', exist_ok=True)
    
    # Desktop screenshot
    create_screenshot(1280, 720, 'screenshots/desktop-screenshot.png', False)
    
    # Mobile screenshot
    create_screenshot(390, 844, 'screenshots/mobile-screenshot.png', True)
    
    print("Screenshots generated successfully!")
    print("Note: These are placeholder screenshots. Replace with actual app screenshots.")

if __name__ == "__main__":
    main()
