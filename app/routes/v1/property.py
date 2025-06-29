from flask import Blueprint
from app.database import get_db
from app.schemas import BuildingOut
from app.services import PropertyService
from flask_pydantic import validate

# Blueprint for property-related routes
property_bp = Blueprint("properties", __name__)

@property_bp.route("<int:property_id>", methods=["GET"])
@validate()
def get_property(property_id) -> BuildingOut:
    """
    Retrieve a property by its ID.

    Args:
        property_id (int): The ID of the property to retrieve.

    Returns:
        BuildingOut: The Pydantic model, which is then serialized
                     to JSON by flask-pydantic.

    Raises:
        404: If the property with the given ID is not found.
    """
    db=get_db()
    building_out = PropertyService.get_by_id(db=db, property_id=property_id)
    return building_out