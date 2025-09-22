# 📱 Enable PWA Installation on Android

## 🔧 **Step 1: Enable Chrome Flags**

### **On Your Android Device:**
1. **Open Chrome browser**
2. **Go to:** `chrome://flags/`
3. **Search for:** `Desktop PWA`
4. **Enable:** `Desktop PWA install`
5. **Search for:** `Web App`
6. **Enable:** `Web App install prompt`
7. **Restart Chrome** (close and reopen)

### **Alternative Flags to Try:**
- `#enable-desktop-pwas`
- `#enable-web-app-install-prompt`
- `#enable-pwa-install-prompt`

## 🔧 **Step 2: Manual Installation**

### **If Install Button Still Doesn't Appear:**
1. **Open Chrome menu** (three dots ⋮)
2. **Look for "Add to Home screen"**
3. **Tap "Add to Home screen"**
4. **Tap "Add" to confirm**

## 🔧 **Step 3: Check PWA Requirements**

### **Your app must have:**
- ✅ **Manifest file** (`/static/manifest.json`)
- ✅ **Service worker** (`/static/sw.js`)
- ✅ **HTTPS** (or localhost)
- ✅ **Valid icons**

## 🔧 **Step 4: Test PWA Features**

### **Check if PWA is working:**
1. **Go to:** `http://192.168.68.116:3000`
2. **Open Chrome DevTools** (F12)
3. **Go to "Application" tab**
4. **Check "Manifest" section**
5. **Check "Service Workers" section**

## 🔧 **Step 5: Alternative Installation**

### **If still not working:**
1. **Use Chrome menu** → "Add to Home screen"
2. **Or use:** `chrome://apps/`
3. **Or use:** Chrome settings → "Site settings"
