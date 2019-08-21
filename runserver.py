"""
This script runs the flask_controller application using a development server.
"""

import time
import os
from flask import Flask, g, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app, logger=False, engineio_logger=False, async_mode='eventlet')

@socketio.on('connect')
def handle_connect():
    print('websocket Client connected!')

@socketio.on('disconnect')
def handle_disconnect():
    print('websocket Client disconnected')

@app.route('/')
@app.route('/remote')
def remote():
    """Renders the remote control page."""
    return render_template(
        'remote.html',
        title='Remote Control')

@app.route('/settings')
def settings_page():
    """Renders the features page."""
    return render_template(
        'settings.html',
        title='Settings',
        message='Try our more advanced features!'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About this project:',
        message='This Web App is meant to control a lirc deamon running on a Raspberry Pi. '
    )

if __name__ == '__main__':
    try:
        socketio.run(app, host="0.0.0.0", port=5555, debug=False)
    except KeyboardInterrupt:
        socketio.stop()
    # finally:
