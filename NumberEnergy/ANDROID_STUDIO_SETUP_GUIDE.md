# Android Studio Setup Guide for Numerology PWA

## 🚀 Overview
This guide will help you convert your Numerology PWA into a native Android app using Capacitor and Android Studio.

## 📋 Prerequisites

### 1. Install Node.js and npm
```bash
# Download and install Node.js from: https://nodejs.org/
# Choose LTS version (recommended)

# Verify installation
node --version
npm --version
```

### 2. Install Android Studio
1. **Download Android Studio** from: https://developer.android.com/studio
2. **Install with default settings**
3. **Open Android Studio** and complete setup wizard
4. **Install Android SDK** (API level 33 or higher recommended)

### 3. Set up Android SDK
1. **Open Android Studio**
2. **Go to:** File → Settings → Appearance & Behavior → System Settings → Android SDK
3. **Install SDK Platforms:** Android 13 (API 33) or higher
4. **Install SDK Tools:** Android SDK Build-Tools, Android SDK Platform-Tools, Android SDK Tools

## 🛠️ Step-by-Step Setup

### Step 1: Install Capacitor CLI
```bash
# Install Capacitor CLI globally
npm install -g @capacitor/cli

# Verify installation
capacitor --version
```

### Step 2: Initialize Capacitor Project
```bash
# Navigate to your project root
cd D:\GitHub\Numerology\NumberEnergy

# Initialize Capacitor
npx cap init "Numerology Analysis" "com.numerology.analysis" --web-dir="mysite/static"

# Add Android platform
npx cap add android
```

### Step 3: Configure Capacitor
Create/edit `capacitor.config.ts`:
```typescript
import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.numerology.analysis',
  appName: 'Numerology Analysis',
  webDir: 'mysite/static',
  server: {
    androidScheme: 'https'
  },
  plugins: {
    SplashScreen: {
      launchShowDuration: 2000,
      backgroundColor: "#1a1a1a",
      showSpinner: false
    },
    StatusBar: {
      style: "dark",
      backgroundColor: "#1a1a1a"
    }
  }
};

export default config;
```

### Step 4: Build Your Flask App for Production
```bash
# Make sure your Flask app is running and accessible
# For local testing, use ngrok or deploy to a server with HTTPS

# Example with ngrok:
# ngrok http 5000
# Note the HTTPS URL (e.g., https://abc123.ngrok-free.app)
```

### Step 5: Configure Capacitor for Your Server
Edit `capacitor.config.ts`:
```typescript
import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.numerology.analysis',
  appName: 'Numerology Analysis',
  webDir: 'mysite/static',
  server: {
    url: 'https://your-ngrok-url.ngrok-free.app', // Replace with your ngrok URL
    cleartext: true
  },
  plugins: {
    SplashScreen: {
      launchShowDuration: 2000,
      backgroundColor: "#1a1a1a",
      showSpinner: false
    },
    StatusBar: {
      style: "dark",
      backgroundColor: "#1a1a1a"
    }
  }
};

export default config;
```

### Step 6: Sync and Open in Android Studio
```bash
# Sync the project
npx cap sync

# Open in Android Studio
npx cap open android
```

## 🎯 Android Studio Configuration

### 1. First Launch
1. **Open Android Studio**
2. **Import project** from `android/` folder
3. **Wait for Gradle sync** to complete
4. **Install any missing SDK components** if prompted

### 2. Configure Build Settings
1. **Go to:** File → Project Structure
2. **Set minimum SDK:** API 21 (Android 5.0)
3. **Set target SDK:** API 33 (Android 13)
4. **Set compile SDK:** API 33

### 3. Configure App Settings
Edit `android/app/src/main/AndroidManifest.xml`:
```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:theme="@style/AppTheme"
        android:usesCleartextTraffic="true">
        
        <activity
            android:name="com.numerology.analysis.MainActivity"
            android:exported="true"
            android:launchMode="singleTask"
            android:theme="@style/AppTheme.NoActionBarLaunch">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
```

## 🚀 Running Your App

### Method 1: Android Studio
1. **Connect Android device** via USB
2. **Enable Developer Options** on your device
3. **Enable USB Debugging**
4. **Click Run** in Android Studio
5. **Select your device** and run

### Method 2: Android Emulator
1. **Create AVD** (Android Virtual Device):
   - Tools → AVD Manager
   - Create Virtual Device
   - Choose device (e.g., Pixel 6)
   - Download system image (API 33)
   - Finish setup
2. **Start emulator**
3. **Run your app**

### Method 3: Command Line
```bash
# Build and run
npx cap run android

# Build only
npx cap build android
```

## 🔧 Troubleshooting

### Common Issues:

#### 1. Gradle Build Failed
```bash
# Clean and rebuild
cd android
./gradlew clean
./gradlew build
```

#### 2. SDK Not Found
- **Open Android Studio**
- **Go to:** File → Settings → Appearance & Behavior → System Settings → Android SDK
- **Install missing SDK components**

#### 3. Device Not Recognized
- **Enable USB Debugging** on device
- **Install device drivers** (Windows)
- **Try different USB cable/port**

#### 4. Network Issues
- **Ensure your Flask app is accessible**
- **Check ngrok URL is correct**
- **Verify HTTPS is working**

## 📱 App Store Preparation

### 1. Generate Signed APK
1. **Go to:** Build → Generate Signed Bundle/APK
2. **Create keystore** (first time)
3. **Choose APK**
4. **Select release build**
5. **Generate APK**

### 2. Test Release Build
```bash
# Build release version
npx cap build android --prod
```

### 3. Upload to Google Play
1. **Create Google Play Console account**
2. **Upload APK/AAB**
3. **Fill app details**
4. **Submit for review**

## 🎨 Customization

### App Icon
Replace `android/app/src/main/res/mipmap-*/ic_launcher.png` with your app icon

### Splash Screen
Edit `android/app/src/main/res/values/styles.xml`:
```xml
<style name="AppTheme" parent="Theme.AppCompat.Light.NoActionBar">
    <item name="android:windowBackground">@drawable/splash</item>
</style>
```

### App Name
Edit `android/app/src/main/res/values/strings.xml`:
```xml
<string name="app_name">Numerology Analysis</string>
```

## 📊 Performance Optimization

### 1. Enable ProGuard
Edit `android/app/build.gradle`:
```gradle
buildTypes {
    release {
        minifyEnabled true
        proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
    }
}
```

### 2. Optimize Images
- **Compress images** in your Flask app
- **Use WebP format** for better compression
- **Implement lazy loading**

### 3. Network Optimization
- **Implement caching** in your Flask app
- **Use CDN** for static assets
- **Optimize API responses**

## 🚨 Important Notes

### Development vs Production
- **Development:** Use ngrok for local testing
- **Production:** Deploy Flask app to server with HTTPS
- **Update server URL** in `capacitor.config.ts`

### Security
- **Use HTTPS** in production
- **Implement proper authentication**
- **Validate all inputs**

### Updates
- **Capacitor updates:** `npm update @capacitor/cli @capacitor/core`
- **Android updates:** Update target SDK regularly
- **Flask app updates:** Deploy to server, app will load new version

## 🎯 Next Steps

1. **Follow this guide step by step**
2. **Test on real device**
3. **Customize app appearance**
4. **Prepare for app store submission**
5. **Monitor app performance**

Your Numerology PWA will now run as a native Android app! 🚀📱
