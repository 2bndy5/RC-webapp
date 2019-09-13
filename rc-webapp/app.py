"""
This script runs the flask_controller application using a development server.

https://flask.palletsprojects.com/en/1.0.x/patterns/flashing/#message-flashing-pattern for flashing tutorial
"""

from flask import Flask, render_template, request, flash, redirect
from flask_login import UserMixin, AnonymousUserMixin, LoginManager, login_required, login_user, logout_user
from flask_socketio import SocketIO, emit

login_manager = LoginManager()
login_manager.login_view = "/login"
socketio = SocketIO(logger=False, engineio_logger=False, async_mode='eventlet')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
login_manager.init_app(app)
socketio.init_app(app)

class Remote:
    def __init__(self, name, link='/remote'):
        self.name = name
        self.link = link

class User(UserMixin):
    def __init__(self, name):
        self.id = name
        self.remotes = []
        self.config = {}
        self._load_config()

    def get_id(self):
        return self.id

    def _load_config(self):
        try:
            with open('backup\\{}.json'.format(self.id), 'r') as acct_file:
                for line in acct_file.readlines():
                    # import from json to self.remotes & self.config
                    print(line)
        except OSError:
            pass # file doesn't exist

class AnonUser(AnonymousUserMixin):
    def __init__(self):
        self.id = 'anonymous'
        self.remotes = []
        self.config = {}

    def get_id(self):
        return self.id

users = {'admin': User(u'admin'), 'anonymous': AnonUser()}
users['admin'].remotes.append(Remote('dummy remote'))

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Renders the login page"""
    if request.method == 'POST':
        form = request.form
        user_name = form.get('username', default=None)
        is_new = bool(form.get('register', default=False))
        if user_name is not None:
            if bool(users.get(user_name)) or is_new: # login
                if is_new and not bool(users.get(user_name)): # add new user
                    users[user_name] = User(user_name)
                    flash('Account created successfully.', 'info')
                if users.get(user_name):
                    login_user(users.get(user_name))
                    flash('Logged in successfully.', 'success')
                    return redirect('remote')
        else:
            flash('username, {}, does not exist!'.format(user_name), 'error')
    return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    """Redirects to login page after logging out"""
    logout_user()
    return render_template("login.html")

@socketio.on('connect')
def handle_connect():
    print('websocket Client connected!')

@socketio.on('disconnect')
def handle_disconnect():
    print('websocket Client disconnected')

@app.route('/remote')
@login_required
def remote():
    """Renders the remote control page."""
    return render_template('remote.html', title='Remote Control')

@app.route('/settings')
@login_required
def settings_page():
    """Renders the settings page."""
    return render_template('settings.html', title='Settings')

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template('about.html', title='About this project:')

if __name__ == '__main__':
    try:
        socketio.run(app, host="0.0.0.0", port=5555, debug=False)
    except KeyboardInterrupt:
        socketio.stop()
