from pydantic import BaseModel, ConfigDict


class StateOut(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class CityOut(BaseModel):
    id: int
    name: str
    state: StateOut

    model_config = ConfigDict(from_attributes=True)

class CityPartOut(BaseModel):
    id: int
    name: str
    city: CityOut

    model_config = ConfigDict(from_attributes=True)