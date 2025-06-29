from flask import Blueprint
from app.database import get_db
from app.schemas import BuildingOut
from app.services import BuildingService
from flask_pydantic import validate

# Blueprint for building-related routes
building_bp = Blueprint("buildings", __name__, url_prefix="/buildings")

@building_bp.route("/<int:building_id>", methods=["GET"])
@validate()
def get_building(building_id) -> BuildingOut:
    """
    Retrieve a building by its ID.

    Args:
        building_id (int): The ID of the building to retrieve.

    Returns:
        BuildingOut: The Pydantic model, serialized to JSON by flask-pydantic.

    Raises:
        404: If the building with the given ID is not found.
    """
    db = get_db()
    building_out = BuildingService.get_by_id(db=db, building_id=building_id)
    return building_out