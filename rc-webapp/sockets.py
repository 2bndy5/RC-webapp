from flask_socketio import SocketIO#, emit

socketio = SocketIO(logger=False, engineio_logger=False, async_mode='eventlet')

@socketio.on('connect')
def handle_connect():
    print('websocket Client connected!')

@socketio.on('disconnect')
def handle_disconnect():
    print('websocket Client disconnected')
