package com.eventapp.webview

import android.app.Service
import android.content.Intent
import android.os.IBinder
import android.webkit.WebView

class WebViewService : Service() {
    
    private var webView: WebView? = null
    
    override fun onCreate() {
        super.onCreate()
        // Initialize WebView for background tasks
        webView = WebView(applicationContext)
    }
    
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        // Handle background tasks
        when (intent?.action) {
            "SYNC_DATA" -> {
                syncDataWithFlaskServer()
            }
            "CACHE_UPDATE" -> {
                updateCache()
            }
            "NOTIFICATION_CHECK" -> {
                checkForNotifications()
            }
        }
        
        return START_STICKY
    }
    
    override fun onBind(intent: Intent?): IBinder? {
        return null
    }
    
    private fun syncDataWithFlaskServer() {
        // Sync data with Flask server in background
        webView?.evaluateJavascript("""
            // Background sync with Flask server
            fetch('/api/sync', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    timestamp: Date.now(),
                    data: localStorage.getItem('eventapp_data')
                })
            }).then(response => {
                if (response.ok) {
                    console.log('Background sync successful');
                }
            }).catch(error => {
                console.error('Background sync failed:', error);
            });
        """, null)
    }
    
    private fun updateCache() {
        // Update local cache
        webView?.evaluateJavascript("""
            // Update cache
            if ('caches' in window) {
                caches.open('eventapp-cache-v1').then(cache => {
                    cache.addAll([
                        '/',
                        '/static/manifest.json',
                        '/static/sw.js'
                    ]);
                });
            }
        """, null)
    }
    
    private fun checkForNotifications() {
        // Check for push notifications
        webView?.evaluateJavascript("""
            // Check for notifications
            fetch('/api/notifications', {
                method: 'GET',
                headers: {'Content-Type': 'application/json'}
            }).then(response => response.json())
            .then(data => {
                if (data.notifications && data.notifications.length > 0) {
                    // Show notifications
                    data.notifications.forEach(notification => {
                        if ('Notification' in window && Notification.permission === 'granted') {
                            new Notification(notification.title, {
                                body: notification.message,
                                icon: '/static/images/icon-192x192.png'
                            });
                        }
                    });
                }
            }).catch(error => {
                console.error('Notification check failed:', error);
            });
        """, null)
    }
    
    override fun onDestroy() {
        super.onDestroy()
        webView?.destroy()
    }
}
