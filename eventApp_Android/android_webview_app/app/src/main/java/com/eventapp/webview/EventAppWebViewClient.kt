package com.eventapp.webview

import android.graphics.Bitmap
import android.net.http.SslError
import android.webkit.*
import android.widget.Toast

class EventAppWebViewClient : WebViewClient() {
    
    override fun shouldOverrideUrlLoading(view: WebView?, request: WebResourceRequest?): Boolean {
        val url = request?.url.toString()
        
        // Handle external URLs
        if (url.startsWith("http://") || url.startsWith("https://")) {
            if (url.contains("eventapp") || url.contains("192.168.68.116")) {
                // Allow internal URLs
                return false
            } else {
                // Open external URLs in external browser
                view?.context?.let { context ->
                    val intent = android.content.Intent(android.content.Intent.ACTION_VIEW, android.net.Uri.parse(url))
                    context.startActivity(intent)
                }
                return true
            }
        }
        
        // Handle deep links
        if (url.startsWith("eventapp://")) {
            handleDeepLink(url)
            return true
        }
        
        return false
    }
    
    override fun onPageStarted(view: WebView?, url: String?, favicon: Bitmap?) {
        super.onPageStarted(view, url, favicon)
        // Show loading indicator if needed
    }
    
    override fun onPageFinished(view: WebView?, url: String?) {
        super.onPageFinished(view, url)
        // Hide loading indicator if needed
        
        // Inject JavaScript for enhanced functionality
        view?.evaluateJavascript("""
            // Enhanced JavaScript for Android WebView
            window.AndroidWebView = {
                // File upload handler
                handleFileUpload: function(filePath) {
                    console.log('File uploaded:', filePath);
                    // Send to Flask server
                    fetch('/api/upload', {
                        method: 'POST',
                        body: new FormData().append('file', filePath)
                    });
                },
                
                // Camera handler
                handleCameraResult: function(imagePath) {
                    console.log('Camera result:', imagePath);
                    // Send to Flask server
                    fetch('/api/camera', {
                        method: 'POST',
                        body: new FormData().append('image', imagePath)
                    });
                },
                
                // Geolocation handler
                getCurrentLocation: function() {
                    if (navigator.geolocation) {
                        navigator.geolocation.getCurrentPosition(
                            function(position) {
                                console.log('Location:', position.coords.latitude, position.coords.longitude);
                                // Send to Flask server
                                fetch('/api/location', {
                                    method: 'POST',
                                    headers: {'Content-Type': 'application/json'},
                                    body: JSON.stringify({
                                        latitude: position.coords.latitude,
                                        longitude: position.coords.longitude
                                    })
                                });
                            },
                            function(error) {
                                console.error('Geolocation error:', error);
                            }
                        );
                    }
                },
                
                // Notification handler
                showNotification: function(title, message) {
                    console.log('Notification:', title, message);
                    // Implement notification logic
                }
            };
            
            // Initialize Android-specific features
            if (typeof window.AndroidWebView !== 'undefined') {
                console.log('Android WebView features loaded');
            }
        """, null)
    }
    
    override fun onReceivedError(view: WebView?, request: WebResourceRequest?, error: WebResourceError?) {
        super.onReceivedError(view, request, error)
        
        val errorMessage = when (error?.errorCode) {
            ERROR_HOST_LOOKUP -> "Cannot connect to server. Please check your network connection."
            ERROR_CONNECT -> "Connection failed. Please check if the Flask server is running."
            ERROR_TIMEOUT -> "Connection timeout. Please try again."
            else -> "An error occurred while loading the page."
        }
        
        view?.context?.let { context ->
            Toast.makeText(context, errorMessage, Toast.LENGTH_LONG).show()
        }
    }
    
    override fun onReceivedSslError(view: WebView?, handler: SslErrorHandler?, error: SslError?) {
        // For development, allow self-signed certificates
        if (error?.primaryError == SslError.SSL_UNTRUSTED) {
            handler?.proceed()
        } else {
            super.onReceivedSslError(view, handler, error)
        }
    }
    
    override fun onReceivedHttpError(view: WebView?, request: WebResourceRequest?, errorResponse: WebResourceResponse?) {
        super.onReceivedHttpError(view, request, errorResponse)
        
        when (errorResponse?.statusCode) {
            404 -> {
                view?.context?.let { context ->
                    Toast.makeText(context, "Page not found. Please check the Flask server.", Toast.LENGTH_LONG).show()
                }
            }
            500 -> {
                view?.context?.let { context ->
                    Toast.makeText(context, "Server error. Please check the Flask server.", Toast.LENGTH_LONG).show()
                }
            }
        }
    }
    
    private fun handleDeepLink(url: String) {
        // Handle deep links like eventapp://event/123
        val path = url.substringAfter("eventapp://")
        when {
            path.startsWith("event/") -> {
                val eventId = path.substringAfter("event/")
                // Navigate to specific event
                // This would be handled by the Flask app
            }
            path.startsWith("user/") -> {
                val userId = path.substringAfter("user/")
                // Navigate to user profile
            }
            else -> {
                // Handle other deep links
            }
        }
    }
}
