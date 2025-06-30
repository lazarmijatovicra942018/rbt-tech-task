from flask import abort, jsonify
from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import Optional, List, Mapping, Any
from .taxonomy import EstateTypeOut, OfferOut, AmenityOut, HeatingOut
from .location import CityPartOut

class BuildingFloorOut(BaseModel):
    building_id: int
    floor_level: Optional[str]
    floor_total: Optional[int]

    model_config = ConfigDict(from_attributes=True)

class BuildingBase(BaseModel):
    square_footage: Optional[float] = None
    construction_year: Optional[int] = None
    land_area: Optional[float] = None
    registration: Optional[bool] = None
    rooms: Optional[float] = None
    bathrooms: Optional[int] = None
    parking: Optional[bool] = None
    price: Optional[int] = None

class BuildingIn(BuildingBase):
    estate_type_id: Optional[int] = None
    offer_id: Optional[int] = None
    city_part_id: Optional[int] = None

    amenity_ids: Optional[list[int]] = []
    heating_ids: Optional[list[int]] = []

class BuildingOut(BuildingBase):
    id: int

    estate_type: EstateTypeOut
    offer: OfferOut
    city_part: Optional[CityPartOut]

    amenities: List[AmenityOut] = []
    heatings: List[HeatingOut] = []

    floor: Optional[BuildingFloorOut] = None

    model_config = ConfigDict(from_attributes=True)


class BuildingSearchQuery(BaseModel):
    """
    Query parameters for searching Building (property) listings,
    plus pagination.
    """

    min_sqft: Optional[int]    = Field(None, ge=0, description="Minimum square footage (>= 0")
    max_sqft: Optional[int]    = Field(None, ge=0, description="Maximum square footage (>= 0)")
    parking: Optional[bool]     = Field(None, description="Whether parking is available")
    state: Optional[str]        = Field(None, description="Name of the state")
    estate_type: Optional[str]  = Field(None, description="Type of property: 'kuća' (house) or 'stan' (apartment)")

    page: int = Field(1, ge=1, description="Page number (1‑indexed)")
    size: int = Field(10, ge=1, le=100, description="Results per page")

    @model_validator(mode="after")
    def check_sqft_range(self) -> "BuildingSearchQuery":
        # instance attributes are already typed/coerced
        if self.min_sqft is not None and self.max_sqft is not None:
            if self.min_sqft > self.max_sqft:
                abort(jsonify({
                    "status": "error",
                    "message": "`min_sqft` must be less than or equal to `max_sqft`"
                }), 422)
        return self


class PaginatedBuildings(BaseModel):
    buildings: list[BuildingOut]
    total: int                   # total matching rows
    page: int                    # current page
    size: int                    # page size
    pages: int                   # total pages = ceil(total/size)