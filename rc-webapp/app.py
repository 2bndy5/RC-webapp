"""
This script runs the flask application.
"""

from flask import Flask
from users import login_manager
from sockets import socketio
from routes import blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
login_manager.init_app(app)
app.register_blueprint(blueprint)
socketio.init_app(app)

if __name__ == '__main__':
    try:
        socketio.run(app, host="0.0.0.0", port=5555, debug=False)
    except KeyboardInterrupt:
        socketio.stop()
