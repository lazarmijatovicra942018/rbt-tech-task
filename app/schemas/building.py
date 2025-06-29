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



class BuildingOut(BaseModel):
    id: int
    square_footage: Optional[float]
    construction_year: Optional[int]
    land_area: Optional[float]
    registration: Optional[bool]
    rooms: Optional[float]
    bathrooms: Optional[int]
    parking: Optional[bool]
    price: Optional[int]

    estate_type: EstateTypeOut
    offer: OfferOut
    city_part: Optional[CityPartOut]

    amenities: List[AmenityOut] = []
    heatings: List[HeatingOut] = []

    floor: Optional[BuildingFloorOut] = None

    model_config = ConfigDict(from_attributes=True)


class BuildingSearchQuery(BaseModel):
    """
    Query parameters for searching Building (property) listings.
    """

    min_sqft: Optional[int]    = Field(None, ge=0, description="minimum square footage")
    max_sqft: Optional[int]    = Field(None, ge=0, description="maximum square footage")
    parking: Optional[bool]     = Field(None, description="True=Yes, False=No")
    state: Optional[str]        = Field(None, description="state name")
    estate_type: Optional[str]  = Field(None, description="'kuća' (house) or 'stan' (apartment)")
    
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