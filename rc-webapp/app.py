"""
This script runs the flask application.
"""

import click
from flask import Flask
from .users import login_manager
from .sockets import socketio
from .routes import blueprint

app = Flask(__name__)
app.secret_key = app.secret_key = b'\x93:\xda\x0cf[\x8c\xc5\xb7D\xa8\xebH\x1d\x9e-7\xca\xe7\x1e\xea\xac\x15.'

# attach the routes to the `app` object
app.register_blueprint(blueprint)

# Enable login management
login_manager.init_app(app)

# Enable WebSocket integration
socketio.init_app(app)

@click.command()
@click.option('--port', default=5555, help='The port number used to access the webapp.')
def run(port):
    try:
        print(f'Hosting @ http://localhost:{port}')
        socketio.run(app, host='0.0.0.0', port=port, debug=False)
    except KeyboardInterrupt:
        socketio.stop()

# due to use of the click decorator
# pylint: disable=no-value-for-parameter
if __name__ == '__main__':
    run()
