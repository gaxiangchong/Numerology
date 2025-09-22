# EventApp Android WebView App

This is a native Android app that wraps your Flask EventApp in a WebView, providing a true standalone APK/AAB that can be installed on Android devices.

## Features

- ✅ **True Native Android App** - APK/AAB file
- ✅ **WebView Integration** - Loads your Flask app
- ✅ **File Upload Support** - Camera, gallery, documents
- ✅ **Geolocation** - GPS location access
- ✅ **Local Storage** - Persistent data storage
- ✅ **Service Worker Support** - Offline caching
- ✅ **Custom WebViewClient** - Enhanced functionality
- ✅ **Deep Link Support** - Custom URL schemes
- ✅ **Background Sync** - Data synchronization
- ✅ **Push Notifications** - Real-time updates

## Project Structure

```
android_webview_app/
├── app/
│   ├── build.gradle
│   ├── src/main/
│   │   ├── java/com/eventapp/webview/
│   │   │   ├── MainActivity.kt
│   │   │   ├── EventAppWebViewClient.kt
│   │   │   ├── EventAppWebChromeClient.kt
│   │   │   └── WebViewService.kt
│   │   ├── res/
│   │   │   ├── layout/activity_main.xml
│   │   │   ├── values/strings.xml
│   │   │   ├── values/themes.xml
│   │   │   ├── values/colors.xml
│   │   │   └── xml/
│   │   └── AndroidManifest.xml
│   └── proguard-rules.pro
├── build.gradle
├── settings.gradle
├── gradle.properties
└── README.md
```

## Setup Instructions

### 1. Prerequisites

- **Android Studio** (latest version)
- **Flask server running** on `192.168.68.116:3000`
- **Android SDK** (API level 24+)

### 2. Configuration

1. **Update Flask Server URL** in `MainActivity.kt`:
   ```kotlin
   private val flaskServerUrl = "http://YOUR_IP:3000"
   ```

2. **Update Package Name** in `build.gradle`:
   ```gradle
   applicationId "com.yourcompany.eventapp"
   ```

3. **Update App Name** in `strings.xml`:
   ```xml
   <string name="app_name">Your EventApp</string>
   ```

### 3. Build and Install

#### Option A: Android Studio
1. Open project in Android Studio
2. Click "Build" → "Build Bundle(s) / APK(s)"
3. Install on device or emulator

#### Option B: Command Line
```bash
cd android_webview_app
./gradlew assembleDebug
```

### 4. Flask Server Integration

Your Flask app should handle these endpoints:

```python
@app.route('/api/upload', methods=['POST'])
def handle_file_upload():
    # Handle file uploads from Android
    pass

@app.route('/api/camera', methods=['POST'])
def handle_camera():
    # Handle camera images from Android
    pass

@app.route('/api/location', methods=['POST'])
def handle_location():
    # Handle GPS location from Android
    pass

@app.route('/api/sync', methods=['POST'])
def handle_sync():
    # Handle background sync
    pass

@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    # Return push notifications
    pass
```

## Advanced Features

### File Upload
- Camera integration
- Gallery access
- Document picker
- Multiple file types

### Geolocation
- GPS coordinates
- Location permissions
- Background location

### Service Worker
- Offline caching
- Background sync
- Push notifications

### Deep Links
- Custom URL schemes
- Event-specific links
- User profile links

## Deployment

### Development
- Install APK directly on device
- Use Android Studio debugger
- Test with Flask server

### Production
- Generate signed APK/AAB
- Upload to Google Play Store
- Or distribute APK directly

## Troubleshooting

### Common Issues

1. **Network Connection**
   - Check Flask server is running
   - Verify IP address in MainActivity.kt
   - Check network permissions

2. **File Upload**
   - Verify file permissions
   - Check file provider configuration
   - Test with different file types

3. **Geolocation**
   - Enable location permissions
   - Test on real device (not emulator)
   - Check GPS settings

4. **Service Worker**
   - Verify HTTPS (for production)
   - Check service worker registration
   - Test offline functionality

### Debug Tips

- Use Chrome DevTools for WebView debugging
- Check Android logs with `adb logcat`
- Test permissions in device settings
- Verify network connectivity

## Security Considerations

- Use HTTPS in production
- Validate file uploads
- Sanitize user input
- Implement proper authentication
- Use secure storage for sensitive data

## Performance Optimization

- Enable WebView caching
- Optimize image loading
- Use lazy loading
- Implement proper error handling
- Monitor memory usage

## Support

For issues or questions:
1. Check Android logs
2. Verify Flask server connectivity
3. Test permissions
4. Review WebView settings
5. Check network configuration
