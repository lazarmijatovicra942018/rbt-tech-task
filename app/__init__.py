from flask import Flask
from app.routes import v1_bp
from app.database import get_db


def create_app():
    """
    Create and configure an instance of the Flask application.

    Returns:
        Flask: Configured Flask application instance.
    """

    app = Flask(__name__)

    from . import database
    database.init_db(app)

    app.register_blueprint(v1_bp, url_prefix="/api/v1")

    return app