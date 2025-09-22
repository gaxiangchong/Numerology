# PowerShell script to set up Numerology PWA for Android Studio
Write-Host "Setting up Numerology PWA for Android Studio..." -ForegroundColor Green
Write-Host ""

Write-Host "Step 1: Installing Capacitor CLI..." -ForegroundColor Yellow
npm install -g @capacitor/cli

Write-Host ""
Write-Host "Step 2: Installing project dependencies..." -ForegroundColor Yellow
npm install

Write-Host ""
Write-Host "Step 3: Initializing Capacitor..." -ForegroundColor Yellow
npx cap init "Numerology Analysis" "com.numerology.analysis" --web-dir="mysite/static"

Write-Host ""
Write-Host "Step 4: Adding Android platform..." -ForegroundColor Yellow
npx cap add android

Write-Host ""
Write-Host "Step 5: Syncing project..." -ForegroundColor Yellow
npx cap sync

Write-Host ""
Write-Host "Setup complete! Next steps:" -ForegroundColor Green
Write-Host "1. Start your Flask app: cd mysite && python app.py" -ForegroundColor Cyan
Write-Host "2. Start ngrok: ngrok http 5000" -ForegroundColor Cyan
Write-Host "3. Update capacitor.config.ts with your ngrok URL" -ForegroundColor Cyan
Write-Host "4. Run: npx cap open android" -ForegroundColor Cyan
Write-Host ""
Write-Host "For detailed instructions, see ANDROID_STUDIO_SETUP_GUIDE.md" -ForegroundColor Magenta

Read-Host "Press Enter to continue"
