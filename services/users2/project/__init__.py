from flask import Flask, Blueprint
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO

from project import settings
from project.api.restplus import api
import os

db = SQLAlchemy()
toolbar = DebugToolbarExtension()
bcrypt = Bcrypt()
socket_io = SocketIO()


def configure_app(app):
    app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def create_app(script_info=None):
    app = Flask(__name__)
    # set config
    configure_app(app)
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    toolbar.init_app(app)

    migrate = Migrate(app, db)
    bcrypt.init_app(app)

    async_mode = os.getenv('ASYNC_MODE')
    socket_io.init_app(app, async_mode=async_mode)

    from project.api.users.enpoints.users import ns as users_blueprint
    blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
    api.init_app(blueprint)
    api.add_namespace(users_blueprint)
    app.register_blueprint(blueprint)
    app.shell_context_processor({'app': app, 'model': db})
    return app
