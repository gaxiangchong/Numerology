#!/usr/bin/env python3
"""
Flask integration endpoints for Android WebView app
Add these routes to your existing Flask app
"""

from flask import Flask, request, jsonify, send_file
import os
import json
from werkzeug.utils import secure_filename
import base64

def add_android_routes(app):
    """Add Android WebView specific routes to your Flask app"""
    
    # File upload endpoint
    @app.route('/api/upload', methods=['POST'])
    def handle_file_upload():
        try:
            if 'file' not in request.files:
                return jsonify({'error': 'No file provided'}), 400
            
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            if file:
                filename = secure_filename(file.filename)
                # Save to uploads directory
                upload_dir = os.path.join(app.static_folder, 'uploads')
                os.makedirs(upload_dir, exist_ok=True)
                file_path = os.path.join(upload_dir, filename)
                file.save(file_path)
                
                return jsonify({
                    'success': True,
                    'filename': filename,
                    'path': file_path,
                    'message': 'File uploaded successfully'
                })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # Camera image endpoint
    @app.route('/api/camera', methods=['POST'])
    def handle_camera():
        try:
            if 'image' not in request.files:
                return jsonify({'error': 'No image provided'}), 400
            
            image = request.files['image']
            if image.filename == '':
                return jsonify({'error': 'No image selected'}), 400
            
            if image:
                filename = secure_filename(image.filename)
                # Save to uploads directory
                upload_dir = os.path.join(app.static_folder, 'uploads')
                os.makedirs(upload_dir, exist_ok=True)
                image_path = os.path.join(upload_dir, filename)
                image.save(image_path)
                
                return jsonify({
                    'success': True,
                    'filename': filename,
                    'path': image_path,
                    'message': 'Image uploaded successfully'
                })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # Geolocation endpoint
    @app.route('/api/location', methods=['POST'])
    def handle_location():
        try:
            data = request.get_json()
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            
            if not latitude or not longitude:
                return jsonify({'error': 'Latitude and longitude required'}), 400
            
            # Store location in database or process as needed
            # For now, just return success
            return jsonify({
                'success': True,
                'latitude': latitude,
                'longitude': longitude,
                'message': 'Location received successfully'
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # Background sync endpoint
    @app.route('/api/sync', methods=['POST'])
    def handle_sync():
        try:
            data = request.get_json()
            timestamp = data.get('timestamp')
            sync_data = data.get('data')
            
            # Process sync data
            # This could involve updating database, processing offline changes, etc.
            
            return jsonify({
                'success': True,
                'timestamp': timestamp,
                'message': 'Sync completed successfully'
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # Notifications endpoint
    @app.route('/api/notifications', methods=['GET'])
    def get_notifications():
        try:
            # Get notifications for the user
            # This is a placeholder - implement your notification logic
            notifications = [
                {
                    'id': 1,
                    'title': 'New Event',
                    'message': 'A new event has been created',
                    'timestamp': '2024-01-01T12:00:00Z'
                },
                {
                    'id': 2,
                    'title': 'Event Reminder',
                    'message': 'Your event starts in 1 hour',
                    'timestamp': '2024-01-01T13:00:00Z'
                }
            ]
            
            return jsonify({
                'success': True,
                'notifications': notifications
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'EventApp API is running',
            'version': '1.0.0'
        })
    
    # CORS headers for Android WebView
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

# Example usage in your main Flask app:
if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    
    # Add Android routes
    add_android_routes(app)
    
    # Your existing routes...
    @app.route('/')
    def index():
        return 'EventApp with Android WebView support'
    
    app.run(host='0.0.0.0', port=3000, debug=True)
