@echo off
echo Setting up Numerology PWA for Android Studio...
echo.

echo Step 1: Installing Capacitor CLI...
npm install -g @capacitor/cli

echo.
echo Step 2: Installing project dependencies...
npm install

echo.
echo Step 3: Initializing Capacitor...
npx cap init "Numerology Analysis" "com.numerology.analysis" --web-dir="mysite/static"

echo.
echo Step 4: Adding Android platform...
npx cap add android

echo.
echo Step 5: Syncing project...
npx cap sync

echo.
echo Setup complete! Next steps:
echo 1. Start your Flask app: cd mysite && python app.py
echo 2. Start ngrok: ngrok http 5000
echo 3. Update capacitor.config.ts with your ngrok URL
echo 4. Run: npx cap open android
echo.
echo For detailed instructions, see ANDROID_STUDIO_SETUP_GUIDE.md
pause
