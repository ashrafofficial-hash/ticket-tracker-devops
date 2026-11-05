
from flask import Flask

from app.extensions import db


def create_app(test_config=None):

    app = Flask(__name__)

    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tickets.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Testing configuration
    if test_config:
        app.config.update(test_config)

    # Initialize database
    db.init_app(app)

    # Import and register routes
    from app.routes import api
    app.register_blueprint(api)

    return app
