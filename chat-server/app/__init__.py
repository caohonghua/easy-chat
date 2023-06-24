from flask import Flask
from flask_socketio import SocketIO
import secrets

socketio = SocketIO(async_mode='gevent', cors_allowed_origins='*')

def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = secrets.token_hex(16)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    return app
    