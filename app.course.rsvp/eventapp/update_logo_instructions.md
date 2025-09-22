# 🎨 Logo Update Instructions

## Current Logo Setup
Your app currently uses a Chinese seal logo located at:
`static/images/logos/chinese-seal.png`

## New Logo Requirements
The new logo should be a red square with four Chinese characters:
- **Top-left:** 卿 (qīng)
- **Top-right:** 合 (hé)
- **Bottom-left:** 文 (wén)
- **Bottom-right:** 化 (huà)

## Steps to Update

### Option 1: Replace the File (Recommended)
1. **Save the new logo image** as `chinese-seal.png`
2. **Replace the existing file** at `static/images/logos/chinese-seal.png`
3. **Keep the same filename** to avoid template changes
4. **Recommended size**: 48x48 pixels (matches current CSS)

### Option 2: Create New Logo File
1. **Create the new logo** with the four characters
2. **Save as PNG format**
3. **Replace** `static/images/logos/chinese-seal.png`
4. **Test the display** in your app

## Logo Specifications
- **Format**: PNG (transparent background preferred)
- **Size**: 48x48 pixels (current CSS size)
- **Background**: Red square
- **Characters**: White or contrasting color
- **Style**: Traditional Chinese seal appearance

## Testing the Update
After updating the logo:
1. **Run your app locally**: `python app.py`
2. **Check the header**: Logo should appear in the top-left
3. **Verify responsiveness**: Logo should scale properly
4. **Test fallback**: If logo fails to load, graduation cap icon should appear

## Deployment
After updating locally:
1. **Commit changes**: `git add . && git commit -m "Update logo"`
2. **Push to repository**: `git push origin main`
3. **Deploy to PythonAnywhere**: Follow deployment guide
4. **Reload web app**: In PythonAnywhere dashboard

## Current Logo CSS (for reference)
```css
.logo-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
  transition: all 0.3s ease;
  overflow: hidden;
}

.logo-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: 8px;
}
```

## Fallback System
Your app has a fallback system:
- **Primary**: Chinese seal logo
- **Fallback**: Graduation cap icon (if logo fails to load)

This ensures your app always displays a logo, even if the image file is missing.
