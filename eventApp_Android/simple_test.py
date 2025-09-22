#!/usr/bin/env python3
"""
Ultra-simple Flask test
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '''
    <h1>🎉 EventApp Test - Working!</h1>
    <p>✅ Flask is running correctly</p>
    <p>✅ Routes are working</p>
    <p>✅ Ready for Android PWA testing</p>
    <br>
    <p><strong>Android URLs:</strong></p>
    <ul>
        <li>Real device: http://192.168.68.116:8080</li>
        <li>Emulator: http://10.0.2.2:8080</li>
    </ul>
    '''

@app.route('/test')
def test():
    return {'status': 'success', 'message': 'EventApp is working!'}

if __name__ == '__main__':
    print("Starting simple test server on port 8080...")
    app.run(host='0.0.0.0', port=8080, debug=True)
