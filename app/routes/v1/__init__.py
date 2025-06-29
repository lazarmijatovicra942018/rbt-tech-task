from flask import Blueprint

# Blueprint for version 1 of the API, grouping all v1 routes
v1_bp = Blueprint("v1", __name__)

from .building import building_bp
v1_bp.register_blueprint(building_bp, url_prefix="/buildings")