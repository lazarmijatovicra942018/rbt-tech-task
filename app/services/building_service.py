from app.models import Building
from sqlalchemy.orm import Session
from app.schemas import BuildingOut
from flask import abort


class BuildingService:
    """
    Service class responsible for building-related operations.

    Handles database interactions for Building records.
    """

    @classmethod
    def get_by_id(cls, db: Session, building_id: int) -> BuildingOut:
        """
        Retrieve a building by its ID from the database.

        Args:
            db (Session): SQLAlchemy database session.
            building_id (int): The ID of the building to retrieve.

        Returns:
            BuildingOut: Pydantic model representing the building.

        Raises:
            404 error: If no building with the given ID is found.
        """

        building_orm = db.get(Building, building_id)
        if building_orm is None:
            abort(404, description=f"Building with ID {building_id} not found")
        building_out = BuildingOut.model_validate(building_orm)
        return building_out
