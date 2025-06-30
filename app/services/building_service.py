from app.models import Building, EstateType, State, City, CityPart, Amenity, Heating
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, and_, func
from app.schemas import BuildingOut, BuildingSearchQuery, PaginatedBuildings
from flask import abort, jsonify, make_response

from app.schemas.building import BuildingIn


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
            payload = {
                "error": "Building not found",
                "id": building_id,
                "message": f"Building with ID {building_id} not found"
            }
            abort(make_response(jsonify(payload), 404))
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

    @classmethod
    def create(cls, db: Session, building_in: BuildingIn) -> BuildingOut:
        """
        Create a new Building and associate existing amenities/heatings.

        Args:
            payload (BuildingCreate): Building data with optional amenity/heating IDs.
            db (Session): Active SQLAlchemy session.

        Returns:
            BuildingRead: The newly created building with nested relations.

        Raises:
            404: If any amenity or heating ID is not found.
            400: On database integrity errors.
        """
        new_building_orm = Building(**building_in.model_dump(
            exclude={"amenity_ids", "heating_ids"}))

        if building_in.amenity_ids:
            stmt = select(Amenity).where(Amenity.id.in_(building_in.amenity_ids))
            new_building_orm.amenities = db.scalars(stmt).all()

            found_amenity_ids = {amenity.id for amenity in new_building_orm.amenities}
            requested_ids = set(building_in.amenity_ids)
            missing = requested_ids - found_amenity_ids
            if missing:
                payload = {
                    "error": "Amenity ID(s) not found",
                    "missing_ids": sorted(missing)
                }

                abort(make_response(jsonify(payload), 404))

        if building_in.heating_ids:
            stmt = select(Heating).where(Heating.id.in_(building_in.heating_ids))
            new_building_orm.heatings = db.scalars(stmt).all()
            found_heating_ids = {heating.id for heating in new_building_orm.heatings}
            requested_ids = set(building_in.heating_ids)
            missing = requested_ids - found_heating_ids
            if missing:
                payload = {
                    "error": "Heating ID(s) not found",
                    "missing_ids": sorted(missing)
                }

                abort(make_response(jsonify(payload), 404))

        try:
            db.add(new_building_orm)
            db.commit()
            db.refresh(new_building_orm)

            return BuildingOut.model_validate(new_building_orm)

        except IntegrityError as e:
            db.rollback()
            payload = {
                "error": "Database integrity error",
                "details": str(e.__cause__ or e),
                "hint": "Check foreign keys or unique constraints",
            }

            abort(make_response(jsonify(payload), 400))