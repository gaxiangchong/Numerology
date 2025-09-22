#!/usr/bin/env python3
"""
Redirect script for rsvp13.pythonanywhere.com to event.mynoblequest.com
This script handles redirects from the old domain to the new domain.
"""

from flask import Flask, redirect, request, url_for
import os

# Create a simple Flask app for redirects
app = Flask(__name__)

@app.route('/')
def redirect_home():
    """Redirect home page to new domain"""
    return redirect('https://event.mynoblequest.com/', code=301)

@app.route('/<path:path>')
def redirect_all(path):
    """Redirect all other paths to new domain"""
    return redirect(f'https://event.mynoblequest.com/{path}', code=301)

@app.route('/static/<path:filename>')
def redirect_static(filename):
    """Redirect static files to new domain"""
    return redirect(f'https://event.mynoblequest.com/static/{filename}', code=301)

@app.route('/templates/<path:filename>')
def redirect_templates(filename):
    """Redirect template files to new domain"""
    return redirect(f'https://event.mynoblequest.com/templates/{filename}', code=301)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
