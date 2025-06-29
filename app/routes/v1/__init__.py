from flask import Blueprint

# Blueprint for version 1 of the API, grouping all v1 routes
v1_bp = Blueprint("v1", __name__)

from .property import property_bp
v1_bp.register_blueprint(property_bp, url_prefix="/properties")