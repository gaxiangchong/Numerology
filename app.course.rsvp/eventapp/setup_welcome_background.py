#!/usr/bin/env python3
"""
Setup Welcome Background Image
This script helps set up the welcome background image.
"""

import os
import shutil

def setup_welcome_background():
    """Setup the welcome background image."""
    print("🖼️ Setting up Welcome Background Image...")
    print("=" * 50)
    
    # Create the backgrounds directory if it doesn't exist
    backgrounds_dir = "static/images/backgrounds"
    if not os.path.exists(backgrounds_dir):
        os.makedirs(backgrounds_dir)
        print(f"✅ Created directory: {backgrounds_dir}")
    
    # Check if the image file exists
    image_path = os.path.join(backgrounds_dir, "welcome-background.jpg")
    
    if os.path.exists(image_path):
        print(f"✅ Background image already exists: {image_path}")
        return True
    else:
        print(f"📁 Image path: {image_path}")
        print("\n📋 Instructions:")
        print("1. Save the attached mountain climbing image as 'welcome-background.jpg'")
        print(f"2. Place it in the directory: {backgrounds_dir}")
        print("3. The image will automatically be used as the welcome section background")
        
        print("\n🎨 Image Requirements:")
        print("• Format: JPG, PNG, or WebP")
        print("• Recommended size: 1920x1080 or larger")
        print("• The image will be automatically resized and positioned")
        
        return False

def show_background_info():
    """Show information about the background setup."""
    print("\n📋 Background Setup Information:")
    print("=" * 50)
    
    print("\n✅ CSS Changes Made:")
    print("• Welcome section now uses the mountain image as background")
    print("• Added dark overlay for better text readability")
    print("• Text is now white with shadow for contrast")
    print("• Background covers the entire section")
    print("• Rounded corners maintained")
    
    print("\n🎨 Visual Effects:")
    print("• Background image: Mountain climbing scene")
    print("• Overlay: Dark gradient for text readability")
    print("• Text: White with shadow for contrast")
    print("• Border: Subtle white border")
    print("• Responsive: Scales with screen size")
    
    print("\n📱 What Users Will See:")
    print("• Beautiful mountain climbing background")
    print("• 'Welcome back, [Name]!' in white text")
    print("• Professional, inspiring appearance")
    print("• Easy to read text over the image")

def main():
    print("🖼️ Welcome Background Image Setup")
    print("=" * 50)
    
    success = setup_welcome_background()
    show_background_info()
    
    if success:
        print("\n🎉 Background image is ready!")
        print("📱 The welcome section will now display the mountain climbing image.")
    else:
        print("\n📋 Next Steps:")
        print("1. Save the attached image as 'welcome-background.jpg'")
        print("2. Place it in the 'static/images/backgrounds/' directory")
        print("3. Refresh the page to see the new background")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
