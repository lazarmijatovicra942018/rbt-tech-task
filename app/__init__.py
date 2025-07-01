from flask import Flask
from flask_apscheduler import APScheduler
from flask_jwt_extended import JWTManager

from app.routes import v1_bp
from app.database import get_db
from app.services import CSVService
from .config import Config

scheduler = APScheduler()
jwt = JWTManager()

def create_app(config_object=Config):
    """
    Create and configure an instance of the Flask application.

    Returns:
        Flask: Configured Flask application instance.
    """

    app = Flask(__name__)
    app.config.from_object(config_object)

    from . import database
    database.init_db(app)

    app.register_blueprint(v1_bp, url_prefix="/api/v1")


    CSVService.init_app(app)

    scheduler.init_app(app)
    scheduler.start()

    jwt.init_app(app)


    return app