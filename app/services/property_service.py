from app.models import Building
from sqlalchemy.orm import Session
from app.schemas import BuildingOut
from flask import abort

class PropertyService:
    """
    Service class responsible for property-related operations.

    This class handles interactions with the database related to
    properties, which correspond to the Building records in the database.
    """

    @classmethod
    def get_by_id(cls, db: Session, property_id: int) -> BuildingOut:
        """
        Retrieve a property by its ID from the database.

        Note:
            Although the API and service use the term "property",
            this corresponds to the "Building" table in the database,
            which stores building/property records.

        Args:
            db (Session): SQLAlchemy database session.
            property_id (int): The ID of the property to retrieve.

        Returns:
            BuildingOut: Pydantic model representing the property.

        Raises:
            404 error: If no property with the given ID is found.
        """

        building_orm = db.get(Building, property_id)
        if building_orm is None:
            abort(404, description=f"Property with ID {property_id} not found")
        building_out = BuildingOut.model_validate(building_orm)
        return building_out