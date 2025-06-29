from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from .taxonomy import EstateTypeOut, OfferOut, AmenityOut, HeatingOut
from .location import CityPartOut

class BuildingFloorOut(BaseModel):
    building_id: int
    floor_level: str
    floor_total: int

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
    city_part: CityPartOut

    amenities: List[AmenityOut] = []
    heatings: List[HeatingOut] = []

    floor: Optional[BuildingFloorOut] = None

    model_config = ConfigDict(from_attributes=True)