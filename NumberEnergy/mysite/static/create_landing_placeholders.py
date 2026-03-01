#!/usr/bin/env python3
"""
Creates placeholder images 001.png–004.png for the landing page.
Run from this directory: python create_landing_placeholders.py
You can replace these files with your own images (same names or update landing.html).
"""
import os

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    # No Pillow: write minimal 1x1 PNG so img tags don't 404
    minimal_png = (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
        b'\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f'
        b'\x00\x00\x01\x01\x00\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    here = os.path.dirname(os.path.abspath(__file__))
    for i in range(1, 5):
        path = os.path.join(here, f'{i:03d}.png')
        with open(path, 'wb') as f:
            f.write(minimal_png)
    print('Created 001.png–004.png (minimal placeholders). Install Pillow for labeled placeholders.')
    exit(0)

HERE = os.path.dirname(os.path.abspath(__file__))
# Hero: wide; Intro: wide; Testimonials: wide strip; Footer: wide
SIZES = [(1200, 500), (1200, 400), (1200, 350), (1200, 300)]
BG = (31, 41, 55)   # surface
TEXT = (229, 231, 235)  # textlight
HIGHLIGHT = (59, 130, 246)

for i, (w, h) in enumerate(SIZES, start=1):
    img = Image.new('RGB', (w, h), BG)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype('arial.ttf', min(w, h) // 8)
    except Exception:
        font = ImageFont.load_default()
    label = f'{i:03d}'
    bbox = draw.textbbox((0, 0), label, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x, y = (w - tw) // 2, (h - th) // 2
    draw.text((x, y), label, fill=TEXT, font=font)
    path = os.path.join(HERE, f'{i:03d}.png')
    img.save(path, 'PNG')
    print(f'Saved {path}')

print('Done. Replace 001.png–004.png with your own images as needed.')
