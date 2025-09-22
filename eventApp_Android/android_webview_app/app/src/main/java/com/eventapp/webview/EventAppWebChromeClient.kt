package com.eventapp.webview

import android.app.Activity
import android.content.Intent
import android.net.Uri
import android.webkit.*
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.core.content.FileProvider
import java.io.File
import java.io.IOException

class EventAppWebChromeClient(private val activity: Activity) : WebChromeClient() {
    
    private var fileUploadCallback: ValueCallback<Array<Uri>>? = null
    private var cameraCallback: ValueCallback<Array<Uri>>? = null
    
    override fun onShowFileChooser(
        webView: WebView?,
        filePathCallback: ValueCallback<Array<Uri>>?,
        fileChooserParams: FileChooserParams?
    ): Boolean {
        
        fileUploadCallback = filePathCallback
        
        val intent = Intent(Intent.ACTION_GET_CONTENT)
        intent.addCategory(Intent.CATEGORY_OPENABLE)
        intent.type = "*/*"
        intent.putExtra(Intent.EXTRA_MIME_TYPES, arrayOf(
            "image/*",
            "application/pdf",
            "text/*",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ))
        
        try {
            if (activity is MainActivity) {
                activity.fileUploadLauncher.launch(intent)
            } else {
                activity.startActivityForResult(intent, 1001)
            }
        } catch (e: Exception) {
            fileUploadCallback = null
            Toast.makeText(activity, "Cannot open file chooser", Toast.LENGTH_SHORT).show()
            return false
        }
        
        return true
    }
    
    override fun onPermissionRequest(request: PermissionRequest?) {
        // Handle permission requests
        request?.let { permissionRequest ->
            val resources = permissionRequest.resources
            val grantedResources = mutableListOf<String>()
            
            // Grant permissions based on what's requested
            for (resource in resources) {
                when (resource) {
                    PermissionRequest.RESOURCE_VIDEO_CAPTURE -> {
                        if (activity.checkSelfPermission(android.Manifest.permission.CAMERA) == 
                            android.content.pm.PackageManager.PERMISSION_GRANTED) {
                            grantedResources.add(resource)
                        }
                    }
                    PermissionRequest.RESOURCE_AUDIO_CAPTURE -> {
                        if (activity.checkSelfPermission(android.Manifest.permission.RECORD_AUDIO) == 
                            android.content.pm.PackageManager.PERMISSION_GRANTED) {
                            grantedResources.add(resource)
                        }
                    }
                    PermissionRequest.RESOURCE_PROTECTED_MEDIA_ID -> {
                        grantedResources.add(resource)
                    }
                }
            }
            
            if (grantedResources.isNotEmpty()) {
                permissionRequest.grant(grantedResources.toTypedArray())
            } else {
                permissionRequest.deny()
            }
        }
    }
    
    override fun onGeolocationPermissionsShowPrompt(
        origin: String?,
        callback: GeolocationPermissions.Callback?
    ) {
        // Handle geolocation permissions
        callback?.invoke(origin, true, false)
    }
    
    override fun onConsoleMessage(consoleMessage: ConsoleMessage?): Boolean {
        // Handle console messages from JavaScript
        consoleMessage?.let { message ->
            val logLevel = when (message.messageLevel()) {
                ConsoleMessage.MessageLevel.ERROR -> "ERROR"
                ConsoleMessage.MessageLevel.WARNING -> "WARNING"
                ConsoleMessage.MessageLevel.LOG -> "LOG"
                ConsoleMessage.MessageLevel.DEBUG -> "DEBUG"
                else -> "INFO"
            }
            
            println("WebView Console [$logLevel]: ${message.message()}")
        }
        
        return true
    }
    
    override fun onProgressChanged(view: WebView?, newProgress: Int) {
        super.onProgressChanged(view, newProgress)
        // Update progress indicator if needed
    }
    
    override fun onReceivedTitle(view: WebView?, title: String?) {
        super.onReceivedTitle(view, title)
        // Update activity title if needed
        title?.let { activity.title = it }
    }
    
    override fun onShowCustomView(view: android.view.View?, callback: CustomViewCallback?) {
        super.onShowCustomView(view, callback)
        // Handle fullscreen video or custom views
    }
    
    override fun onHideCustomView() {
        super.onHideCustomView()
        // Hide custom view
    }
    
    // Handle file upload result
    fun handleFileUploadResult(uri: Uri?) {
        uri?.let { fileUri ->
            fileUploadCallback?.onReceiveValue(arrayOf(fileUri))
        } ?: run {
            fileUploadCallback?.onReceiveValue(null)
        }
        fileUploadCallback = null
    }
    
    // Handle camera result
    fun handleCameraResult(uri: Uri?) {
        uri?.let { imageUri ->
            cameraCallback?.onReceiveValue(arrayOf(imageUri))
        } ?: run {
            cameraCallback?.onReceiveValue(null)
        }
        cameraCallback = null
    }
    
    // Create camera intent
    fun createCameraIntent(): Intent {
        val intent = Intent(android.provider.MediaStore.ACTION_IMAGE_CAPTURE)
        
        try {
            val photoFile = createImageFile()
            val photoURI = FileProvider.getUriForFile(
                activity,
                "${activity.packageName}.fileprovider",
                photoFile
            )
            intent.putExtra(android.provider.MediaStore.EXTRA_OUTPUT, photoURI)
        } catch (e: IOException) {
            e.printStackTrace()
        }
        
        return intent
    }
    
    private fun createImageFile(): File {
        val imageFileName = "JPEG_${System.currentTimeMillis()}_"
        val storageDir = activity.getExternalFilesDir(android.os.Environment.DIRECTORY_PICTURES)
        return File.createTempFile(imageFileName, ".jpg", storageDir)
    }
}
