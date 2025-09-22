package com.eventapp.webview

import android.Manifest
import android.annotation.SuppressLint
import android.app.Activity
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Bundle
import android.webkit.*
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.webkit.WebViewAssetLoader
import com.eventapp.webview.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {
    
    private lateinit var binding: ActivityMainBinding
    private lateinit var webView: WebView
    private lateinit var assetLoader: WebViewAssetLoader
    
    // Flask server configuration
    private val flaskServerUrl = "http://192.168.68.116:3000" // Change this to your Flask server IP
    private val localAssetsDomain = "appassets.androidplatform.net"
    
    // File upload result launcher
    internal val fileUploadLauncher = registerForActivityResult(
        ActivityResultContracts.StartActivityForResult()
    ) { result ->
        if (result.resultCode == Activity.RESULT_OK) {
            val data: Intent? = result.data
            val uri: Uri? = data?.data
            if (uri != null) {
                handleFileUpload(uri)
            }
        }
    }
    
    // Camera result launcher
    internal val cameraLauncher = registerForActivityResult(
        ActivityResultContracts.StartActivityForResult()
    ) { result ->
        if (result.resultCode == Activity.RESULT_OK) {
            val data: Intent? = result.data
            val uri: Uri? = data?.data
            if (uri != null) {
                handleCameraResult(uri)
            }
        }
    }
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        
        setupWebView()
        setupAssetLoader()
        requestPermissions()
    }
    
    @SuppressLint("SetJavaScriptEnabled")
    private fun setupWebView() {
        webView = binding.webView
        
        // Enable JavaScript
        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true
        webView.settings.databaseEnabled = true
        //webView.settings.cacheMode = WebSettings.LOAD_DEFAULT
        webView.settings.cacheMode = WebSettings.LOAD_DEFAULT
        // Enable mixed content (HTTP/HTTPS)
        webView.settings.mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
        
        // Enable file access
        webView.settings.allowFileAccess = true
        webView.settings.allowContentAccess = true
        webView.settings.allowFileAccessFromFileURLs = true
        webView.settings.allowUniversalAccessFromFileURLs = true
        
        // Enable geolocation
        webView.settings.setGeolocationEnabled(true)
        
        // Disable zoom for full-screen app experience
        webView.settings.setSupportZoom(false)
        webView.settings.builtInZoomControls = false
        webView.settings.displayZoomControls = false
        
        // Set viewport for mobile optimization
        webView.settings.useWideViewPort = true
        webView.settings.loadWithOverviewMode = true
        
        // Enable hardware acceleration
        webView.setLayerType(WebView.LAYER_TYPE_HARDWARE, null)
        
        // Set user agent to mobile
        webView.settings.userAgentString = "Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36 EventApp-Android"
        
        // Set custom WebViewClient
        webView.webViewClient = EventAppWebViewClient()
        
        // Set custom WebChromeClient
        webView.webChromeClient = EventAppWebChromeClient(this)
        
        // Load the Flask app with full-screen parameters
        val urlWithParams = "$flaskServerUrl?mobile=1&standalone=1&fullscreen=1"
        webView.loadUrl(urlWithParams)
    }
    
    private fun setupAssetLoader() {
        assetLoader = WebViewAssetLoader.Builder()
            .setDomain(localAssetsDomain)
            .setHttpAllowed(true)
            .build()
    }
    
    private fun requestPermissions() {
        val permissions = arrayOf(
            Manifest.permission.INTERNET,
            Manifest.permission.ACCESS_NETWORK_STATE,
            Manifest.permission.READ_EXTERNAL_STORAGE,
            Manifest.permission.WRITE_EXTERNAL_STORAGE,
            Manifest.permission.CAMERA,
            Manifest.permission.ACCESS_FINE_LOCATION,
            Manifest.permission.ACCESS_COARSE_LOCATION,
            Manifest.permission.POST_NOTIFICATIONS
        )
        
        val permissionsToRequest = permissions.filter {
            ContextCompat.checkSelfPermission(this, it) != PackageManager.PERMISSION_GRANTED
        }
        
        if (permissionsToRequest.isNotEmpty()) {
            ActivityCompat.requestPermissions(this, permissionsToRequest.toTypedArray(), 1001)
        }
    }
    
    private fun handleFileUpload(uri: Uri) {
        // Handle file upload to Flask server
        val filePath = getRealPathFromURI(uri)
        if (filePath != null) {
            // Send file to Flask server
            webView.evaluateJavascript(
                "window.handleFileUpload('$filePath');", null
            )
        }
    }
    
    private fun handleCameraResult(uri: Uri) {
        // Handle camera result
        val filePath = getRealPathFromURI(uri)
        if (filePath != null) {
            webView.evaluateJavascript(
                "window.handleCameraResult('$filePath');", null
            )
        }
    }
    
    private fun getRealPathFromURI(uri: Uri): String? {
        return try {
            contentResolver.query(uri, null, null, null, null)?.use { cursor ->
                val nameIndex = cursor.getColumnIndex(android.provider.OpenableColumns.DISPLAY_NAME)
                cursor.moveToFirst()
                cursor.getString(nameIndex)
            }
        } catch (e: Exception) {
            e.printStackTrace()
            null
        }
    }
    
    override fun onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack()
        } else {
            super.onBackPressed()
        }
    }
    
    override fun onDestroy() {
        super.onDestroy()
        webView.destroy()
    }
}
