from app.models import Building, EstateType, State, City, CityPart
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, func
from app.schemas import BuildingOut, BuildingSearchQuery, PaginatedBuildings
from flask import abort, jsonify


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

    @classmethod
    def search(cls, db: Session, filters: BuildingSearchQuery) -> PaginatedBuildings:
        """
        Search buildings with optional filters and return paginated results.

        Args:
            db (Session): SQLAlchemy database session.
            filters (BuildingSearchQuery): Filtering and pagination parameters.

        Returns:
            PaginatedBuildings: Pydantic model containing:
                - buildings: List of BuildingOut items for the requested page.
                - total: Total number of matching buildings.
                - page: Current page number (clamped to valid range).
                - size: Number of items per page.
                - pages: Total number of available pages.
        """
        stmt = select(Building)
        conditions = []
        
        if filters.estate_type is not None:
            stmt = stmt.join(Building.estate_type)
            conditions.append(EstateType.name == filters.estate_type)
            
        if filters.state is not None:
            stmt = (
                stmt
                .join(Building.city_part)
                .join(CityPart.city)
                .join(City.state)
            )
            conditions.append(State.name == filters.state)
        
        if filters.min_sqft is not None:
            conditions.append(Building.square_footage >= filters.min_sqft)
        
        if filters.max_sqft is not None:
            conditions.append(Building.square_footage <= filters.max_sqft)
        
        if filters.parking is not None:
            conditions.append(Building.parking == filters.parking)
        
        if conditions:
            stmt = stmt.where(and_(*conditions))

        #Pagination
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = db.scalar(count_stmt) or 0

        size = filters.size
        pages = max((total + size - 1) // size, 1)

        page = min(max(filters.page, 1), pages)
        offset = (page - 1) * size

        paged_stmt = stmt.order_by(Building.id).limit(size).offset(offset)

        results = db.scalars(paged_stmt).all()
        buildings_out = [BuildingOut.model_validate(building_orm) for building_orm in results]


        return PaginatedBuildings(
            buildings=buildings_out,
            total=total,
            page=page,
            size=size,
            pages=pages
        )