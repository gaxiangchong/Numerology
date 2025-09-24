import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.numerology.analysis',
  appName: 'Numerology Analysis',
  webDir: 'mysite/static',
  // Use HTTPS with proper configuration for live server
  server: {
    url: 'https://bazipro.pythonanywhere.com',
    cleartext: false,
    allowNavigation: ['https://bazipro.pythonanywhere.com/*']
  },
  android: {
    allowMixedContent: true,
    captureInput: true,
    webContentsDebuggingEnabled: true,
    overrideUserAgent: 'CapacitorApp',
    appendUserAgent: 'CapacitorApp',
    useLegacyBridge: true
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
