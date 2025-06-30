from flask import Blueprint, jsonify
from app.database import get_db
from app.schemas import BuildingOut, BuildingSearchQuery, PaginatedBuildings
from app.schemas.building import BuildingIn
from app.services import BuildingService
from flask_pydantic import validate, ValidationError

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


@building_bp.route("/search", methods=["GET"])
@validate(
    query=BuildingSearchQuery
)
def search_buildings(query: BuildingSearchQuery) -> PaginatedBuildings:
    """
    Search for buildings using query parameters such as square footage, parking,
    state, and estate type.

    Args:
        query (BuildingSearchQuery): The validated query parameters from the URL.

    Returns:
        PaginatedBuildings: A paginated list of buildings matching the filters,
                            including total results, current page, and total pages.

    Raises:
        422: If query parameters are invalid (e.g. min_sqft > max_sqft).
    """

    db = get_db()
    return BuildingService.search(db=db, filters=query)

@building_bp.route("", methods=["POST"])
@validate(body=BuildingIn)
def create_building(body: BuildingIn) -> BuildingOut:
    """
    Create a new building record.

    Args:
        body (BuildingIn): Pydantic schema containing building data
            and lists of existing amenity and heating IDs.

    Returns:
        BuildingOut: The created building, with nested relations,
            serialized to JSON by flask-pydantic.

    Raises:
        404: If any provided amenity or heating ID does not exist.
        400: On database integrity errors (e.g., FK or unique-constraint failures).
    """
    db = get_db()
    new_building_out = BuildingService.create(db=db, building_in=body)
    return  new_building_out


@building_bp.route("/<int:building_id>", methods=["PUT"])
@validate(body=BuildingIn)
def update_building(building_id: int, body: BuildingIn) -> BuildingOut:
    """
    Update an existing building record.

    Args:
        building_id (int): The ID of the building to update.
        body (BuildingIn): Pydantic schema containing the fields to update,
            including optional lists of existing amenity and heating IDs.

    Returns:
        BuildingOut: The updated building, with nested relations,
            serialized to JSON by flask-pydantic.

    Raises:
        404: If the building with `building_id` does not exist, or if any
            provided amenity or heating ID does not exist.
        400: On database integrity errors (e.g., foreign‑key or unique‑constraint failures).
    """
    db = get_db()
    updated_building_out = BuildingService.update(db=db, building_id=building_id, building_in=body)
    return updated_building_out